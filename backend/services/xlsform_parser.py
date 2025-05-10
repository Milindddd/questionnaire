import pandas as pd
from fastapi import UploadFile
from typing import Dict, List, Any, Optional
import uuid
from models.form import ParsedForm, FormGroup, Question
import logging

logger = logging.getLogger(__name__)

class XLSFormParser:
    REQUIRED_SHEETS = ['survey', 'choices']
    REQUIRED_SURVEY_COLUMNS = ['type', 'name', 'label']
    REQUIRED_CHOICES_COLUMNS = ['list_name', 'name', 'label']

    async def validate_file(self, file: UploadFile) -> bool:
        """
        Validate if the uploaded file follows XLSForm structure
        """
        try:
            # Read Excel file
            df_dict = pd.read_excel(file.file, sheet_name=None)
            
            # Check required sheets
            if not all(sheet in df_dict for sheet in self.REQUIRED_SHEETS):
                logger.error("Missing required sheets")
                return False
            
            # Validate survey sheet
            survey_df = df_dict['survey']
            if not all(col in survey_df.columns for col in self.REQUIRED_SURVEY_COLUMNS):
                logger.error("Missing required columns in survey sheet")
                return False
            
            # Validate choices sheet
            choices_df = df_dict['choices']
            if not all(col in choices_df.columns for col in self.REQUIRED_CHOICES_COLUMNS):
                logger.error("Missing required columns in choices sheet")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False
        finally:
            await file.seek(0)

    async def parse_file(self, file: UploadFile) -> ParsedForm:
        """
        Parse XLSForm Excel file into structured form data
        """
        try:
            # Read Excel file
            df_dict = pd.read_excel(file.file, sheet_name=None)
            
            # Parse survey sheet
            survey_df = df_dict['survey']
            choices_df = df_dict['choices']
            settings_df = df_dict.get('settings')
            
            # Get form metadata
            form_id = str(uuid.uuid4())
            form_title = self._get_form_title(survey_df)
            form_version = self._get_form_version(settings_df)
            
            # Parse questions and groups
            groups = self._parse_groups(survey_df, choices_df)
            
            # Parse settings
            settings = self._parse_settings(settings_df) if settings_df is not None else None
            
            return ParsedForm(
                id=form_id,
                title=form_title,
                version=form_version,
                groups=groups,
                settings=settings
            )
            
        except Exception as e:
            logger.error(f"Error parsing file: {str(e)}")
            raise
        finally:
            await file.seek(0)

    def _get_form_title(self, survey_df: pd.DataFrame) -> Dict[str, str]:
        """Extract form title from survey sheet"""
        title_row = survey_df[survey_df['type'] == 'form_title'].iloc[0] if not survey_df[survey_df['type'] == 'form_title'].empty else None
        if title_row is not None:
            return {'default': title_row.get('label', 'Untitled Form')}
        return {'default': 'Untitled Form'}

    def _get_form_version(self, settings_df: Optional[pd.DataFrame]) -> str:
        """Extract form version from settings sheet"""
        if settings_df is not None and 'version' in settings_df.columns:
            version_row = settings_df[settings_df['form_id'] == 'version'].iloc[0] if not settings_df[settings_df['form_id'] == 'version'].empty else None
            if version_row is not None:
                return str(version_row.get('value', '1.0.0'))
        return '1.0.0'

    def _parse_groups(self, survey_df: pd.DataFrame, choices_df: pd.DataFrame) -> List[FormGroup]:
        """Parse form groups and their questions"""
        groups: List[FormGroup] = []
        current_group = None
        
        for _, row in survey_df.iterrows():
            if row['type'] == 'begin_group':
                current_group = {
                    'name': row['name'],
                    'label': {'default': row['label']},
                    'questions': [],
                    'appearance': row.get('appearance'),
                    'relevant': row.get('relevant')
                }
            elif row['type'] == 'end_group':
                if current_group:
                    groups.append(FormGroup(**current_group))
                    current_group = None
            elif current_group is not None and row['type'] not in ['note', 'form_title']:
                question = self._parse_question(row, choices_df)
                current_group['questions'].append(question)
            elif row['type'] not in ['note', 'form_title'] and current_group is None:
                # Questions not in any group go to a default group
                if not groups or groups[-1].name != 'default':
                    groups.append(FormGroup(
                        name='default',
                        label={'default': 'Default Group'},
                        questions=[]
                    ))
                question = self._parse_question(row, choices_df)
                groups[-1].questions.append(question)
        
        return groups

    def _parse_question(self, row: pd.Series, choices_df: pd.DataFrame) -> Question:
        """Parse individual question from survey row"""
        question_data = {
            'type': row['type'],
            'name': row['name'],
            'label': {'default': row['label']},
            'required': row.get('required', '').lower() == 'yes',
            'appearance': row.get('appearance'),
            'relevant': row.get('relevant'),
            'calculation': row.get('calculation'),
            'default': row.get('default'),
            'hint': {'default': row.get('hint')} if row.get('hint') else None
        }
        
        # Add choices for select questions
        if 'select' in row['type']:
            list_name = row.get('list_name')
            if list_name:
                choices = choices_df[choices_df['list_name'] == list_name]
                question_data['choices'] = [
                    {
                        'name': choice['name'],
                        'label': {'default': choice['label']}
                    }
                    for _, choice in choices.iterrows()
                ]
        
        # Add constraints if present
        if row.get('constraint'):
            question_data['constraints'] = {
                'rule': row['constraint'],
                'message': {'default': row.get('constraint_message', '')}
            }
        
        return Question(**question_data)

    def _parse_settings(self, settings_df: pd.DataFrame) -> Dict[str, Any]:
        """Parse form settings"""
        if settings_df is None:
            return {}
            
        settings = {}
        for _, row in settings_df.iterrows():
            if 'form_id' in row and 'value' in row:
                settings[row['form_id']] = row['value']
        return settings 