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

  $.get('https://127.0.0.1:5001/api/v1/status/', function (data, status) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error('Error fetching API status: ' + textStatus + ', ' + errorThrown);
  });

  $.ajax({
    type: 'POST',
    url: 'https://127.0.0.1:5001/api/v1/places_search/',
    data: '{}',
    success: function (data) {
      for (let i = 0; i < data.length; i++) {
        const article = `
          <article data-id="${data[i].id}">
            <div class="title_box">
              <h2>${data[i].name}</h2>
              <div class="price_by_night">$${data[i].price_by_night}</div>
            </div>
            <div class="information">
              <div class="max_guest">${data[i].max_guest} Guests</div>
              <div class="number_rooms">${data[i].number_rooms} Bedrooms</div>
              <div class="number_bathrooms">${data[i].number_bathrooms} Bathrooms</div>
            </div>
            <div class="image_hotel" style="background-image: url('../../static/images/${data[i].image}')" aria-label="image of ${data[i].name}"></div>
            <div class="description">${data[i].description}</div>
            <div class="reviews">
              <h2>Reviews　<span class="showReview" data-id="${data[i].id}">show</span></h2>
              <ul data-id="${data[i].id}"></ul>
            </div>
          </article>
        `;
        $('section.places').append(article);
      }
    },
    contentType: 'application/json'
  });

  $('button').click(function () {
    $('section.places').empty();
    $.ajax({
      type: 'POST',
      url: 'https://127.0.0.1:5001/api/v1/places_search/',
      data: JSON.stringify({ amenities: Object.keys(dicoa), states: Object.keys(dicos), cities: Object.keys(dicoc) }),
      success: function (data) {
        for (let i = 0; i < data.length; i++) {
          const article = `
            <article data-id="${data[i].id}">
              <div class="title_box">
                <h2>${data[i].name}</h2>
                <div class="price_by_night">$${data[i].price_by_night}</div>
              </div>
              <div class="information">
                <div class="max_guest">${data[i].max_guest} Guests</div>
                <div class="number_rooms">${data[i].number_rooms} Bedrooms</div>
                <div class="number_bathrooms">${data[i].number_bathrooms} Bathrooms</div>
              </div>
              <div class="image_hotel" style="background-image: url('../../static/images/${data[i].image}')"></div>
              <div class="description">${data[i].description}</div>
              <div class="reviews">
                <h2>Reviews <span class="showReview" data-id="${data[i].id}">show</span></h2>
                <ul data-id="${data[i].id}"></ul>
              </div>
            </article>
          `;
          $('section.places').append(article);
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
    const showReviewElement = $(this);
    
    $.get(`https://127.0.0.1:5001/api/v1/places/${placeid}/reviews`, function (data) {
      const ulElement = $(`ul[data-id="${placeid}"]`);
      
      if (showReviewElement.text() === 'show') {
        ulElement.empty();
        for (let i = 0; i < data.length; i++) {
          ulElement.append(`<li>${data[i].text}</li>`);
        }
        showReviewElement.text('hide');
      } else {
        ulElement.empty();
        showReviewElement.text('show');
      }
    });
  });

  $(document).on('click', 'article', function () {
    const placeId = $(this).attr('data-id');
    if (placeId) {
      window.location.href = `/places/${placeId}`;
    }
  });
  $(document).on('click', '#api_status', function () {
    $('#api_status').click(function() {
        $.ajax({
            url: '/check_login_status',  // ログイン状態をチェックするエンドポイント
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.logged_in) {
                  window.location.href = `/user/${data.user_id}`;
                } else {
                    window.location.href = '/login';  // ログインしていない場合のリダイレクト先
                }
            },
            error: function(xhr, status, error) {
                console.error('Error checking login status:', error);
                // ログインチェックに失敗した場合の処理を追加することも可能
            }
        });
    });
  });
});
