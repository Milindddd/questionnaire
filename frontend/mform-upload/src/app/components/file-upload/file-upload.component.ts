import { Component, Output, EventEmitter, Input } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})
export class FileUploadComponent {
  @Output() fileSelected = new EventEmitter<File>();
  @Input() isLoading = false;
  isDragging = false;
  
  constructor(private snackBar: MatSnackBar) {}

  onFileDropped(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  onFileSelected(event: Event) {
    const element = event.target as HTMLInputElement;
    const files = element.files;
    
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  handleFile(file: File) {
    if (this.isLoading) {
      return;
    }

    if (this.isValidFile(file)) {
      this.fileSelected.emit(file);
    } else {
      this.snackBar.open('Please upload a valid Excel file (.xls/.xlsx)', 'Close', {
        duration: 3000
      });
    }
  }

  isValidFile(file: File): boolean {
    const validTypes = [
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ];
    return validTypes.includes(file.type);
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    if (!this.isLoading) {
      this.isDragging = true;
    }
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }
} 