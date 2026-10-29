"""Genera index.html y contacto.html a partir de las pantallas de Stitch (src/stitch-*.html)."""
import re, pathlib
root = pathlib.Path(__file__).parent
PHONE_WA = "573104567890"

def common(h):
    # logos reales
    h = re.sub(r'<img src="https://lh3[^"]*"[^>]*alt="Productos[^"]*"[^>]*>',
               '<img src="assets/logo-banner.jpg" alt="Productos Químicos Mi Fragancia S.A.S." class="h-10 md:h-12 w-auto object-contain rounded">', h)
    h = re.sub(r'<img src="https://lh3[^"]*"[^>]*>',
               '<img src="assets/logo-banner.jpg" alt="Productos Químicos Mi Fragancia S.A.S." class="h-12 w-auto object-contain">', h)
    # head: CSS local en vez de CDN de Tailwind
    h = re.sub(r'<script src="https://cdn.tailwindcss.com"></script><script id="tailwind-config">.*?</script>',
               '<link rel="stylesheet" href="assets/styles.css">', h, flags=re.S)
    h = h.replace('<meta content="web_standard" name="shell-type">', '<meta name="description" content="Distribución de productos químicos, aseo institucional y tratamiento de piscinas en Valledupar, Cesar."><link rel="icon" href="assets/logo-icon.jpg">')
    h = h.replace('</body>', '<script src="assets/site.js" defer></script></body>')
    # navegación
    nav = {"inicio": "index.html", "servicios": "index.html#servicios", "productos": "index.html#catalogo",
           "piscinas": "index.html#servicios", "mantenimiento": "index.html#servicios", "contacto": "contacto.html",
           "cotizar-por-whatsapp": f"https://wa.me/{PHONE_WA}?text=Hola,%20quiero%20cotizar%20productos%20Mi%20Fragancia"}
    for k, v in nav.items():
        h = re.sub(r'(data-path="%s"[^>]*?)href="#"' % k, r'\1href="%s"' % v, h)
        h = re.sub(r'href="#"([^>]*?data-path="%s")' % k, r'href="%s"\1' % v, h)
    h = h.replace('href="https://wa.me/573001234567"', f'href="https://wa.me/{PHONE_WA}"')
    h = h.replace("+57 (300) 123-4567", "+57 310 456 7890")
    h = re.sub(r'<a href="#"( class="flex items-center">)', r'<a href="index.html"\1', h)
    return h

# --- Inicio
h = common((root / "src/stitch-inicio.html").read_text())
icons = ["water_drop", "pool", "cleaning_services", "science"]
n = [0]
def img(m):
    i = n[0]; n[0] += 1
    if i == 0:
        return ('<div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-cyan-200 via-sky-400 to-blue-700">'
                '<img src="assets/logo-icon.jpg" alt="Mi Fragancia" class="w-40 h-40 rounded-3xl shadow-2xl object-cover"></div>')
    return (f'<div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-sky-50 to-sky-200">'
            f'<span class="material-symbols-outlined text-primary" style="font-size:88px;color:#1d4ed8">{icons[i-1]}</span></div>')
h = re.sub(r'<img class="w-full h-full object-cover" data-alt="[^"]*" src="[^"]*">', img, h)
h = h.replace('<section class="w-full py-space-xl lg:py-24 bg-surface">', '<section id="servicios" class="w-full py-space-xl lg:py-24 bg-surface">', 1)
h = h.replace('<section class="w-full py-space-xl bg-surface-container-low">', '<section id="nosotros" class="w-full py-space-xl bg-surface-container-low">', 1)
h = h.replace('href="https://maps.google.com/?q=Carrera+9+19-50+Valledupar+Cesar"', 'href="contacto.html#mapa"', 0)
IFR = ('<iframe title="Mapa Mi Fragancia" class="absolute inset-0 w-full h-full border-0" loading="lazy" '
       'src="https://www.openstreetmap.org/export/embed.html?bbox=-73.2560%2C10.4660%2C-73.2340%2C10.4810&amp;layer=mapnik&amp;marker=10.4735%2C-73.2450"></iframe>')
h = h.replace('<!-- Simulated Map Overlay Controls -->', IFR + '<!-- Simulated Map Overlay Controls -->', 1)
h = h.replace('<div class="absolute top-4 left-4 p-space-md rounded-xl', '<div class="absolute z-10 top-4 left-4 p-space-md rounded-xl', 1)
h = h.replace('<!-- Pulsing Pin Indicator -->\n<div class="absolute top-1/2', '<!-- Pulsing Pin Indicator -->\n<div class="hidden absolute top-1/2', 1)
(root / "index.html").write_text(h)

# --- Contacto
h = common((root / "src/stitch-contacto.html").read_text())
h = re.sub(r' onsubmit="[^"]*"', '', h, count=1)
h = re.sub(r'<div class="absolute inset-0 w-full h-full bg-cover bg-center" data-location[^>]*></div>',
           '<iframe title="Mapa Mi Fragancia" class="absolute inset-0 w-full h-full border-0" loading="lazy" '
           'src="https://www.openstreetmap.org/export/embed.html?bbox=-73.2560%2C10.4660%2C-73.2340%2C10.4810&amp;layer=mapnik&amp;marker=10.4735%2C-73.2450"></iframe>', h, count=1)
h = re.sub(r'<div class="flex flex-col gap-1.5 bg-surface-container-lowest/90[^>]*>(?:(?!</div>).)*?Aumentar zoom.*?Reducir zoom.*?</button>\s*</div>', '', h, count=1, flags=re.S)
h = h.replace('<div class="relative w-full rounded-2xl overflow-hidden shadow-lg', '<div id="mapa" class="relative w-full rounded-2xl overflow-hidden shadow-lg', 1)
(root / "contacto.html").write_text(h)
