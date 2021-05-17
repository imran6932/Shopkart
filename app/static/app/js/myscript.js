$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    responsiveClass: true,
    dots:false,
    responsive: {
        0: {
            items: 1,
            nav: true,
            autoplay: true,
        },
        600: {
            items: 2,
            nav: true,
            autoplay: true,
        },
        800: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1200: {
            items: 5,
            nav: true,
            autoplay: true,
        }
    }
});

// Plus Cart
$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("shipping").innerText = data.shipping_charge
            document.getElementById("totalamount").innerText = data.totalamount
            document.getElementById("discount").innerText = data.discount
        }
    });
});

// Minus Cart
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("shipping").innerText = data.shipping_charge
            document.getElementById("totalamount").innerText = data.totalamount
            document.getElementById("discount").innerText = data.discount
        }
    });
});

// Remove cart
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type:"GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            if (data.status == 1){
                eml.parentNode.parentNode.parentNode.parentNode.remove()
            }            
            document.getElementById("amount").innerText = data.amount
            document.getElementById("shipping").innerText = data.shipping_charge
            document.getElementById("totalamount").innerText = data.totalamount
            document.getElementById("discount").innerText = data.
            discount          
            document.getElementById("remove-cart").innerText = data.totalitem
        }
    });
});