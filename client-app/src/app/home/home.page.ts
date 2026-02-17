import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, 
  IonItem, IonLabel, IonInput, IonButton, 
  IonList, IonThumbnail 
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  standalone: true,
  imports: [
    CommonModule, FormsModule, 
    IonHeader, IonToolbar, IonTitle, IonContent, 
    IonItem, IonLabel, IonInput, IonButton, 
    IonList, IonThumbnail
  ]
})
export class HomePage implements OnInit {
  // Queste servono per i campi di testo dell'HTML
  tavoloInput: string = '';
  nomeInput: string = '';

  // Queste servono per la logica dopo il login
  tavolo: string = '';
  nome: string = '';
  prodotti: any[] = [];
  
  // METTI IL TUO URL DELLA PORTA 5000 (Senza lo / finale)
  apiUrl = 'https://obscure-space-acorn-wrv6pjq9w77wc97p-5000.app.github.dev';

  constructor(private http: HttpClient) {}

  ngOnInit() { 
    this.http.get(this.apiUrl + '/prodotti').subscribe({
      next: (data: any) => this.prodotti = data,
      error: (err) => console.error("Errore caricamento:", err)
    }); 
  }

  login(t: string, n: string) {
    if (t && n) {
      this.tavolo = t;
      this.nome = n;
    }
  }

  ordina(p: any) {
    const body = { tavolo: this.tavolo, cliente: this.nome };
    this.http.post(this.apiUrl + '/ordini', body).subscribe(() => {
      alert('Ordine di ' + p.nome + ' inviato!');
    });
  }
}