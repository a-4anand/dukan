// Mobile navigation works even when the optional jQuery/Bootstrap scripts are unavailable.
(function () {
    function setupMobileNavigation() {
        var menuButton = document.querySelector('.navbar-toggler');
        var mobileMenu = document.getElementById('navbarSupportedContent');
        if (!menuButton || !mobileMenu || menuButton.dataset.menuReady === 'true') return;

        menuButton.dataset.menuReady = 'true';
        var lastTouchAt = 0;
        function toggleMobileMenu(event) {
            if (event && event.type === 'click' && Date.now() - lastTouchAt < 600) return;
            var isOpen = mobileMenu.classList.toggle('show');
            menuButton.setAttribute('aria-expanded', String(isOpen));
        }
        menuButton.addEventListener('click', toggleMobileMenu);
        menuButton.addEventListener('touchend', function (event) {
            event.preventDefault();
            lastTouchAt = Date.now();
            toggleMobileMenu(event);
        }, { passive: false });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupMobileNavigation);
    } else {
        setupMobileNavigation();
    }
}());

// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    var yearNode = document.querySelector("#displayYear");
    if (yearNode) yearNode.innerHTML = currentYear;
}

getYear();


// isotope js
$(window).on('load', function () {
    if (!$.fn.isotope) return;
    $('.filters_menu li').click(function () {
        $('.filters_menu li').removeClass('active');
        $(this).addClass('active');

        var data = $(this).attr('data-filter');
        $grid.isotope({
            filter: data
        })
    });

    var $grid = $(".grid").isotope({
        itemSelector: ".all",
        percentPosition: false,
        masonry: {
            columnWidth: ".all"
        }
    })
});

// nice select
$(document).ready(function() {
    if ($.fn.niceSelect) $('select').niceSelect();
  });

/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// client section owl carousel
if ($.fn.owlCarousel && $(".client_owl-carousel").length) $(".client_owl-carousel").owlCarousel({
    loop: true,
    margin: 0,
    dots: false,
    nav: true,
    navText: [],
    autoplay: true,
    autoplayHoverPause: true,
    navText: [
        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
    ],
    responsive: {
        0: {
            items: 1
        },
        768: {
            items: 2
        },
        1000: {
            items: 2
        }
    }
});
