$(document).ready(function(){
    $('.add-wishlist').click(function(e){
        e.preventDefault();

        var product_id=$(this).data('product');
        var token = $('input[name=csrfmiddlewaretoken]').val();
        // Ajax
        $.ajax({
            method:"POST",
            url:"/add_wishlist",
            data:{
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            dataType:'json',
            success:function(res){
                alertify.success(res.status)
            }
            
        });
    });

    $('.delete-wishlist-item').click(function(e){
        e.preventDefault();
    
        var product_id=$(this).data('product');
        console.log(product_id)
        var token = $('input[name=csrfmiddlewaretoken]').val();
        // Ajax
        $.ajax({
            method:"POST",
            url:"/delete-wishlist-item",
            data:{
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            dataType:'json',
            success:function(res){
                alertify.success(res.status)
                window.location.reload();
            }
                
        });
    });
});


