$('document').ready(function () {
  const dicoa = {};
  const dicos = {};
  const dicoc = {};
  $('.amenities input[type="checkbox"]').change(function () {
    if (this.checked === true) {
      dicoa[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete dicoa[$(this).attr('data-id')];
    }
    $('.amenities h4').text(Object.values(dicoa).join(', '));
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
<div class=price_by_night>$${data[i].price_by_night}</div>
</div>
<div class=information>
<div class=max_guest>${data[i].max_guest} Guests</div>
<div class=number_rooms>${data[i].number_rooms} Bedrooms</div>
<div class=number_bathrooms>${data[i].number_bathrooms} Bathrooms</div>
</div>
<div class=description>
${data[i].description}
</div>
<div class="reviews">
<h2>Reviews <span class="showReview" data-id=${data[i].id}>show</span></h2>
<ul data-id=${data[i].id}>
</ul>
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
      data: JSON.stringify({ amenities: Object.keys(dicoa), states: Object.keys(dicos), cities: Object.keys(dicoc) }),
      success: function (data) {
        for (let i = 0; i < data.length; i++) {
          $('section.places').append(`
<article>
<div class=title_box>
<h2>${data[i].name}</h2>
<div class=price_by_night>$${data[i].price_by_night}</div>
</div>
<div class=information>
<div class=max_guest>${data[i].max_guest} Guests</div>
<div class=number_rooms>${data[i].number_rooms} Bedrooms</div>
<div class=number_bathrooms>${data[i].number_bathrooms} Bathrooms</div>
</div>
<div class=description>
${data[i].description}
</div>
<div class="reviews">
<h2>Reviews <span class="showReview" data-id=${data[i].id}>show</span></h2>
<ul data-id=${data[i].id}>
</ul>
</div>
</article>
`);
        }
      },
      contentType: 'application/json'
    });
  });
  $('input[type="checkbox"].stateinput').change(function () {
    if (this.checked === true) {
      dicos[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete dicos[$(this).attr('data-id')];
    }
    $('.locations h4').empty();
    $('.locations h4').text(Object.values(dicos).join(', '));
  });
  $('input[type="checkbox"].cityinput').change(function () {
    if (this.checked === true) {
      dicoc[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete dicoc[$(this).attr('data-id')];
    }
    $('.locations h4').empty();
    $('.locations h4').text(Object.values(dicoc).join(', '));
  });
  $(document).on('click', '.reviews .showReview', function () {
    const placeid = $(this).attr('data-id');
    $.get(`http://0.0.0.0:5001/api/v1/places/${placeid}/reviews`, function (data) {
      if ($(`.showReview[data-id=${placeid}]`).text() === 'show') {
        for (let i = 0; i < data.length; i++) {
          $(`ul[data-id=${placeid}]`).append(`<li>${data[i].text}</li>`);
        }
        $(`.showReview[data-id=${placeid}]`).text('hide');
      } else {
        $(`.reviews ul[data-id=${placeid}]`).empty();
        $(`.showReview[data-id=${placeid}]`).text('show');
      }
    });
  });
});
