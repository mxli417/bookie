# Bookie-Dokumentation

Diese Dokumentation erklärt den fachlichen Kern des Projekts unabhängig von
der Streamlit-Oberfläche. Alle Beträge sind fiktive Spielpunkte.

## Einstieg

1. [Pricing, Overround und Bookmaker-Risiko](pricing-and-risk.md)
   erklärt den Weg von fairen Wahrscheinlichkeiten zu angebotenen Quoten,
   grenzt Overround von realisiertem Gewinn ab und beschreibt die
   Acceptance Policy.
2. Die [README](../README.md) enthält Installation, Startbefehle,
   Projektstruktur und Roadmap.
3. Die ausführbaren Beispiele liegen in `src/bookie/sim/runner.py` und in der
   lokalen Streamlit-Anwendung `src/bookie/web.py`.

## Leitgedanke

> Ein Buchmacher muss das nächste Ergebnis nicht kennen. Er muss die
> Wahrscheinlichkeitsverteilung vernünftig bepreisen und einen Book führen,
> dessen mögliche Verluste seine Risikotragfähigkeit nicht überschreiten.

Das ist keine Garantie für Gewinn. Fehlerhafte Wahrscheinlichkeiten,
einseitiger Order Flow, Korrelationen und seltene Extremereignisse bleiben
reale Risiken. Genau diese Trennung zwischen Prognose und Risikosteuerung soll
der kleine Engine-Kern sichtbar machen.
