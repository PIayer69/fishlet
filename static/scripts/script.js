function update_no_questions(){
    terms_div = $('.terms')
    no_questions_input = $('.no_questions_input')
    no_questions = terms_div.find('p').length
    no_questions_input.val(no_questions)
}

function get_no_questions(){
    terms_div = $('.terms')
    no_questions = terms_div.find('p').length

    return no_questions
}

function get_last_term_index(){
    terms_div = $('.terms')
    terms = terms_div.find('p')
    last_term = terms[terms.length - 1]
    return parseInt(last_term.childNodes[1].getAttribute('name').split('-')[1])
}

$(document).ready(function(){
    update_no_questions()
    no_questions = get_no_questions()
    last_term_index = no_questions

    $('.terms-button').click(function(){
        p = $('<p/>').appendTo('.terms')
        $('<input/>', {
            'type': 'text',
            'name':`name-${last_term_index + 1}`,
            'placeholder': 'Term',
            'required': 'True'
        }).appendTo(p)
        $('<input/>', {
            'type': 'text',
            'name':`def-${last_term_index + 1}`,
            'placeholder': 'Definition',
            'required': 'True'
        }).appendTo(p)
        $('<span/>', {
            'class': 'delete-term',
            'id': last_term_index+1,
            'data-url': '/delete-term/',
            'text': 'X'
        }).appendTo(p)
        last_term_index += 1
        update_no_questions()
    })


    $('.terms').on('click', 'span.delete-term', function(){
        // console.log($(this).parent())
        // $(this).parent().remove()
        // console.log(url)
        url = $(this).attr('data-url')
        term_p = $(this).parent()
        if(url == '/delete-term/'){
            term_p.remove()
            update_no_questions()
        }
        else{
            $.ajax({
                url: url,
                type: 'GET',
                success:function(data, textStatus, jqXHR){
                    term_p.remove()
                    update_no_questions()
                },
                error:function(xhr, status, error){
                    alert('failed')
                }
            })
        }
        last_term_index = get_last_term_index()
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
        $('<a/>', {
            'id':'myDiv',
            'class':'myClass',
            'href': url,
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

    
})