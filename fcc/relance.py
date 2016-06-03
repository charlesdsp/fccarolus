"""
Batch pour envoi du mail de relance.

Vérifie que le jour est le jeudi (jour 4) avant d'envoyer le mail.
"""

import mechanize
import date


def reload():
    """Appel de l'url de relance."""
    jour = date.isoweekday()
    if jour == 4:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open('http://www.fccarolus/fcc/relance')
