# Manual Reader

Ein sicheres System zur Anzeige von Reparaturleitfäden (PDFs) im Browser.

## Features
- **View-only PDF Viewer**: Canvas-basiertes Rendering ohne Download-/Druckfunktion.
- **Dynamische Wasserzeichen**: Benutzer-E-Mail und Zeitstempel auf jeder Seite.
- **Sicherheits-Auth**: Nur eine aktive Sitzung pro Benutzer.
- **Gerätebindung**: Administrator-Freigabe für neue Geräte erforderlich.
- **Einladungssystem**: Registrierung nur mit Administrator-generierten Codes.
- **Admin Dashboard**: Volle Kontrolle über Benutzer, PDFs und Einladungen.

## Tech Stack
- **Backend**: Django 5.x
- **Frontend**: Tailwind CSS, Alpine.js, PDF.js
- **Datenbank**: MySQL
- **Deployment**: Docker & Docker Compose

## Installation (Docker)

1. Repository klonen
2. Docker Compose starten:
   ```bash
   docker-compose up --build
   ```
3. Migrationen ausführen:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
4. Superuser erstellen:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Projektstruktur
- `apps/accounts`: Benutzerverwaltung & Sicherheit
- `apps/manuals`: PDF-Logik & Viewer
- `apps/invitations`: Einladungscode-System
- `apps/dashboard`: Administrator-Oberfläche
