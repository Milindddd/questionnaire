import { Component, Input } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

interface Question {
  type: string;
  name: string;
  label: { [key: string]: string };
  required: boolean;
  constraints?: {
    rule: string;
    message: { [key: string]: string };
  };
  choices?: Array<{
    name: string;
    label: { [key: string]: string };
  }>;
  appearance?: string;
  relevant?: string;
  calculation?: string;
  default?: any;
  hint?: { [key: string]: string };
}

interface FormGroup {
  name: string;
  label: { [key: string]: string };
  questions: Question[];
  appearance?: string;
  relevant?: string;
}

interface ParsedForm {
  id: string;
  title: { [key: string]: string };
  version: string;
  groups: FormGroup[];
  settings?: { [key: string]: any };
  metadata?: { [key: string]: any };
}

@Component({
  selector: 'app-form-preview',
  templateUrl: './form-preview.component.html',
  styleUrls: ['./form-preview.component.scss']
})
export class FormPreviewComponent {
  @Input() form: ParsedForm | null = null;
  expandedGroups: Set<string> = new Set();

  constructor(private snackBar: MatSnackBar) {}

  toggleGroup(groupName: string): void {
    if (this.expandedGroups.has(groupName)) {
      this.expandedGroups.delete(groupName);
    } else {
      this.expandedGroups.add(groupName);
    }
  }

  isGroupExpanded(groupName: string): boolean {
    return this.expandedGroups.has(groupName);
  }

  downloadJson(): void {
    if (!this.form) return;

    try {
      const jsonString = JSON.stringify(this.form, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      
      link.href = url;
      link.download = `${this.form.id || 'form'}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      this.snackBar.open('Form JSON downloaded successfully', 'Close', {
        duration: 3000
      });
    } catch (error) {
      this.snackBar.open('Error downloading form JSON', 'Close', {
        duration: 5000
      });
    }
  }

  getQuestionIcon(type: string): string {
    switch (type) {
      case 'text':
        return 'text_fields';
      case 'number':
        return 'pin';
      case 'select_one':
        return 'radio_button_checked';
      case 'select_multiple':
        return 'check_box';
      case 'date':
        return 'calendar_today';
      case 'time':
        return 'schedule';
      case 'image':
        return 'image';
      case 'geopoint':
        return 'location_on';
      default:
        return 'help_outline';
    }
  }
} 