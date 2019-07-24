const delete_item_button = document.querySelectorAll('.profile-file-delete');
delete_item_button.forEach(function(btn) {
    btn.addEventListener('click', function(e){
        console.log('fire!')
        e.stopPropagation()
        delete_item = btn.parentNode.parentNode
        delete_item_id = delete_item.querySelector('.profile-file-id')
        fetch("http://localhost:8000/share/delete/"+delete_item_id.innerHTML, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data['status']);
            if (data['status'] == 'success'){
                delete_item.remove();
            }
        })
        .catch(error => console.error('Error:', error));
    })
})

