$(document).ready(function(){
    $('#Nariai .container-3 .carousel').slick({
        draggable: false,
        autoplay: true,
        autoplaySpeed: 5000,
        speed: 1000,
        dots: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        prevArrow: '<span class="priv_arrow"><img src="../images/left button.svg" alt="previous"></i></span>',
        nextArrow: '<span class="next_arrow"><img src="../images/right button.svg" alt="next"></span>',
        
        responsive: [
            {
                // screens greater than >= 1200px
                breakpoint: 1600,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 860,
                settings: {
                    arrows: false,
                    draggable: true,
                    slidesToShow: 2,
                }
            }
        ]
    });  
});
