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
  $.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
});
