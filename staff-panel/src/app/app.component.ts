import { Component, OnInit, signal } from '@angular/core'; // Aggiunto signal
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  // Trasformiamo l'array in un Signal
  ordini = signal<any[]>([]);
  
  apiUrl = 'https://obscure-space-acorn-wrv6pjq9w77wc97p-5000.app.github.dev';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.caricaOrdini();
    // Refresh ogni 3 secondi
    setInterval(() => this.caricaOrdini(), 3000);
  }

  caricaOrdini() {
    this.http.get(this.apiUrl + '/ordini').subscribe({
      next: (data: any) => {
        console.log("Dati ricevuti e salvati nel signal:", data);
        // Usiamo .set() per aggiornare il signal
        this.ordini.set(data);
      },
      error: (err) => console.error("Errore:", err)
    });
  }

  aggiornaStato(id: number, nuovoStato: string) {
    this.http.post(this.apiUrl + '/stato/' + id, { stato: nuovoStato }).subscribe(() => {
      this.caricaOrdini();
    });
  }
}