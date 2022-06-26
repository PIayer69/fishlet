$(document).ready(function(){
    path = window.location.pathname
    form = $('form')
    previousData = form.serialize()
    status_div = $('.status')


    //Updating links for deleteing terms after autosave
    //id - span id
    //q_id - question id in db
    function update_links(id, q_id){
        term = $('.terms').find('p')[id-1].children[2]
        attr = term.getAttribute('data-url')
        // console.log(attr)
        if(attr == '/delete-term/'){
            attr = attr + q_id
            term.setAttribute('data-url', attr)
        }
    }


    //Updating time since last autosave
    function update_status(){
        status = status_div.text()
        if(!status.search(/Saved( [1-6]s)?/)){
            seconds = parseInt(status[6])
            if(isNaN(seconds)){
                seconds = 1
            }
            else{
                seconds += 1
            }
            status_div.text(`Saved ${seconds}s ago`)
        }
    }


    //Checking for new changes in edit form
    //Then submiting it to the backend
    function check_changes(){
        status_div.text('Checking for changes...')
        newData = form.serialize()
        
        if(previousData != newData){
            previousData = form.serialize()
            
            formData = new FormData(document.querySelector('form'))
            $.ajax({
                url: path,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success:function(data, textStatus, jqXHR){
                    response = data
                    if(response['changed']){
                        status_div.html('Saved')
                    }
                    else{
                        status_div.html('Unchanged')
                    }

                    delete response['changed']
                    console.log(response)
                    $.each(response, function(question_id, input_id){
                        update_links(input_id, question_id)
                    })
                },
                error: function(jqXHR, textStatus, errorThrown){
                    status_div.text('<red>Error</red>')
                }
            })
        }
        else{
            status_div.text('Unchanged')
        }
    }


    

    setInterval(check_changes, 5000)
    setInterval(update_status, 1000)

})