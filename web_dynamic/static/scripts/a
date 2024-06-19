$('document').ready(function () {
  const dico = {};
  $('input[type="checkbox"]').change(function () {
    if (this.checked === true) {
      dico[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete dico[$(this).attr('data-id')];
    }
    $('.amenities h4').text(Object.values(dico).join(', '));
  });
});
