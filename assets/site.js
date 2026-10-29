// Formulario de contacto: arma el pedido y lo envía por WhatsApp (número de la empresa).
(function () {
  var WA = '573104567890';
  var form = document.getElementById('contact-form');
  if (!form) return;
  var box = document.getElementById('confirmation-box');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var g = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; };
    var subj = document.getElementById('contact-subject');
    var tipo = subj && subj.selectedIndex > 0 ? subj.options[subj.selectedIndex].text : '';
    var lines = ['Hola, soy ' + g('contact-name') + '.', 'Tipo de solicitud: ' + tipo, g('contact-msg'),
      'Teléfono: ' + g('contact-phone'), g('contact-email') && 'Correo: ' + g('contact-email')].filter(Boolean);
    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    if (box) box.classList.remove('hidden');
    form.reset();
  });
})();
