$(document).ready(function () {
    const amenities = {};
    $('input:checkbox').click(function () {
        $(this).each(function () {
            if (this.checked) {
                amenities[$(this).data('id')] = $(this).data('name');
            } else {
                delete amenities[$(this).data('id')];
            }
        });
        if (Object.values(amenities).length > 0) {
            $('.amenities h4').text(Object.values(amenities).join(', '));
        }else {
            $('.amenities h4').html('&nbsp;');
        }
    });
});

$.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
    console.log(data);
    if (data.status === 'OK') {
        $('DIV#api_status').addClass('available');
    } else {
        $('DIV#api_status').removeClass('available');
    }
});
 const users = {};
 $.getJSON('http://0.0.0.0:5001/api/v1/users/', function (data) {
    for (const user of data) {
        users[user.id] = user.first_name + ' ' + user.last_name;
    }
});

$.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search',
    contentType: 'application/json',
    dataType: 'json',
    data: '{}',
    success: function (data) {
        for (const place of Object.values(data)) {
            $('section.places').append('<article><div class="title"><h2>' + place.name + '</h2><div class="price_by_night">' + place.price_by_night + '</div></div><div class="information">' + '<div class="max_guest">' + '<i class="fa fa-users fa-3x" aria-hidden="true"></i><br />' + place.max_guest + ' Guests</div>' + '<div class="number_rooms">' + '<i class="fa fa-bed fa-3x" aria-hidden="true"></i><br />' + place.number_rooms + ' Bedrooms</div>' + '<div class="number_bathrooms">' + '<i class="fa fa-bath fa-3x" aria-hidden="true"></i><br />' + place.number_bathrooms + 'Bathroom</div>' + '</div><div class="user"><strong>Owner: ' + `${users[place.user_id]}</strong></div>` + '<div class="description">' + place.description + '</div></article>');
            }        
        }
});

$('button').click(function () {
    $.ajax({
        type: 'POST',
        url: 'http://0.0.0.0:5001/api/v1/places_search',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({ amenities: Object.keys(amenities) }),
        success: function (data) {
            $('article').remove();
            for (const place of Object.values(data)) {
                $('section.places').append('<article><div class="title"><h2>' + place.name + '</h2><div class="price_by_night">' + place.price_by_night + '</div></div><div class="information">' + '<div class="max_guest">' + '<i class="fa fa-users fa-3x" aria-hidden="true"></i><br />' + place.max_guest + ' Guests</div>' + '<div class="number_rooms">' + '<i class="fa fa-bed fa-3x" aria-hidden="true"></i><br />' + place.number_rooms + ' Bedrooms</div>' + '<div class="number_bathrooms">' + '<i class="fa fa-bath fa-3x" aria-hidden="true"></i><br />' + place.number_bathrooms + 'Bathroom</div>' + '</div><div class="user"><strong>Owner: ' + `${users[place.user_id]}</strong></div>` + '<div class="description">' + place.description + '</div></article>');
        }
    }
    })
});