$(document).ready(function(){
    // banner image change
    let bannerCount = 0;
    setInterval(function(){
        hideAllBanner();
        changeBannerCount();
        changeBanner();
    }, 8000);

    function changeBanner(){
        $('.banner-item').each(function(idx){
            if(bannerCount == idx){
                $(this).addClass('active-banner');
            }
        });
    }

    function hideAllBanner(){
        $('.banner-item').each(function(idx){
            $(this).removeClass('active-banner');
        });
    }

    // $(document).ready(function() {
    //   $('#signup-form').submit(function(event) {
    //     event.preventDefault();
    //     var formData = $(this).serialize();
    //     $.ajax({
    //       type: 'POST',
    //       url: '/signup',
    //       data: formData,
    //       success: function(response) {
    //         if ('error' in response) {
    //           $('#error-message').show();
    //         } else {
    //           window.location.href = '/login';
    //         }
    //       },
    //       error: function(response) {
    //         console.log(response);
    //       }
    //     });
    //   });
    // });
    
    


    //       // adopt me js
    // var adoptBtn = document.querySelector('.adopt-1');
    // adoptBtn.addEventListener('click', showDetails);

  

    var yearsInput = document.getElementById("age-years");
  var monthsInput = document.getElementById("age-months");
  
  yearsInput.addEventListener('input', validateInput);
  monthsInput.addEventListener('input', validateInput);
  
  function validateInput() {
    var yearsVal = yearsInput.value;
    var monthsVal = monthsInput.value;
    
    if (yearsVal == 0 && monthsVal == 0) {
      yearsInput.setCustomValidity('Either years or months must be greater than 0.');
      monthsInput.setCustomValidity('Either years or months must be greater than 0.');
    } else {
      yearsInput.setCustomValidity('');
      monthsInput.setCustomValidity('');
    }
  }

    function changeBannerCount(){
        bannerCount++;
        if(bannerCount >= $('.banner-item').length){
            bannerCount = 0;
        }
    }

  

    // navigation bar toggle
    $('#navbar-toggler').click(function(){
        $('.navbar-collapse').slideToggle(500);
    });

    // fixed navbar 
    $(window).scroll(function(){
        let pos = $(window).scrollTop();
        if(pos >710){
            $('.navbar').addClass('fxd-navbar');
        } else {
            $('.navbar').removeClass('fxd-navbar');
        }
    });
});
