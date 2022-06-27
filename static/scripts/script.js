$(document).ready(function(){
    var csrftoken = $.cookie('csrftoken')
    var document_url = document.location.origin

    $('.terms-button').click(function(){
        p = $('<p/>').appendTo('.terms')
        $('<input/>', {
            'type': 'text',
            'name':`name`,
            'placeholder': 'Term',
            'required': 'True'
        }).appendTo(p)
        $('<input/>', {
            'type': 'text',
            'name':`def`,
            'placeholder': 'Definition',
            'required': 'True'
        }).appendTo(p)
        $('<span/>', {
            'class': 'delete-term',
            'data-url': '/delete-term/',
            'text': 'X'
        }).appendTo(p)
    })


    $('.terms').on('click', 'span.delete-term', function(){
        // console.log($(this).parent())
        // $(this).parent().remove()
        // console.log(url)
        url = $(this).attr('data-url')
        term_p = $(this).parent()
        if(url == '/delete-term/'){
            term_p.remove()
        }
        else{
            $.ajax({
                url: url,
                type: 'POST',
                headers:{'X-CSRFToken': csrftoken},
                success:function(data, textStatus, jqXHR){
                    term_p.remove()
                },
                error:function(xhr, status, error){
                    alert('failed')
                }
            })
        }
    })


    $('.delete-button').click(function(){
        url = $(this).attr('data-url')
        name = $(this).attr('data-name')
        $('<div/>', {
            'class': 'dimmed',
        }).appendTo('body')
        $('<div/>', {
            'class': 'delete-box',
            'text': `Are you sure you want to delete "${name}"?`
        }).appendTo('.dimmed')
        $('<div/>', {
            'class': 'delete-box-buttons',
        }).appendTo('.delete-box')
        $('<span/>', {
            'class':'delete-box-delete-button',
            'data-url': url,
            'text':`Delete`,
        }).appendTo('.delete-box-buttons');
        $('<div/>', {
            'class':'close-box-button',
            'text':`Close`,
            'onclick': 'close_box()'
        }).appendTo('.delete-box-buttons');
    })

    $(document).on('click', '.close-box-button', function(){
        $('.dimmed').remove()
    })

    $(document).on('click', '.delete-box-delete-button', function(){
        url = $(this).data('url')
        $.ajax({
            url: url,
            type: 'POST',
            headers:{'X-CSRFToken': csrftoken},
            success:function(data, textStatus, jqXHR){
                window.location.replace(document_url)
            },
            error:function(xhr, status, error){
                alert('failed')
            }
        })
        $('.dimmed').remove()
    })
    
})