import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FileService } from './services/file.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(
    private fileService: FileService,
    private snackBar: MatSnackBar
  ) {}

  onFileSelected(file: File) {
    this.fileService.validateFile(file).subscribe({
      next: (response) => {
        if (response.valid) {
          this.uploadFile(file);
        } else {
          this.snackBar.open('Invalid file format. Please check the file structure.', 'Close', {
            duration: 5000
          });
        }
      },
      error: (error) => {
        this.snackBar.open('Error validating file. Please try again.', 'Close', {
          duration: 5000
        });
      }
    });
  }

  private uploadFile(file: File) {
    this.fileService.uploadFile(file).subscribe({
      next: (response) => {
        this.snackBar.open('File uploaded successfully!', 'Close', {
          duration: 3000
        });
      },
      error: (error) => {
        this.snackBar.open('Error uploading file. Please try again.', 'Close', {
          duration: 5000
        });
      }
    });
  }
} 