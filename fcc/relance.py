import mechanize


def reload():
    """Appel de l'url de relance."""
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('http://www.fccarolus/fcc/relance')
