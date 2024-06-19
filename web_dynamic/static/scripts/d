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
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    data: '{}',
    success: function (data) {
      for (let i = 0; i < data.length; i++) {
        $('section.places').append(`
<article>
<div class=title_box>
<h2>${data[i].name}</h2>
<div class=price_by_night>${data[i].price_by_night}$</div>
</div>
<div class=information>
<div class=max_guest>${data[i].max_guest} Guests</div>
<div class=number_rooms>${data[i].number_rooms} Bedrooms</div>
<div class=number_bathrooms>${data[i].number_bathrooms} Bathrooms</div>
</div>
<div class=description>
${data[i].description}
</div>
</article>
`);
      }
    },
    contentType: 'application/json'
  });
  $('button').click(function () {
    $('section.places').empty();
    $.ajax({
      type: 'POST',
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      data: JSON.stringify({ amenities: Object.keys(dico) }),
      success: function (data) {
        for (let i = 0; i < data.length; i++) {
          $('section.places').append(`
<article>
<div class=title_box>
<h2>${data[i].name}</h2>
<div class=price_by_night>${data[i].price_by_night}$</div>
</div>
<div class=information>
<div class=max_guest>${data[i].max_guest} Guests</div>
<div class=number_rooms>${data[i].number_rooms} Bedrooms</div>
<div class=number_bathrooms>${data[i].number_bathrooms} Bathrooms</div>
</div>
<div class=description>
${data[i].description}
</div>
</article>
`);
        }
      },
      contentType: 'application/json'
    });
  });
});
