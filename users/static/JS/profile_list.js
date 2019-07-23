delete_item_button = document.querySelector('.profile-file-delete')
delete_item = delete_item_button.parentNode.parentNode
delete_item_id = delete_item.querySelector('.profile-file-id')
delete_item_button.addEventListener('click', function(e){
    fetch("http://localhost:8000/share/delete/"+delete_item_id.innerHTML)
    .then(response => response.json())
    .then(data => {
        console.log(data['status']);
        if (data['status'] == 'success'){
            delete_item.remove();
        }
    })
})

