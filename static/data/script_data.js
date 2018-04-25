function delete_data(e) {
    title = e.getElementsByClassName('title_to_delete')[0].innerText;
    console.log(title)
    document.getElementById('delete_title').value = title;
    var result = confirm("Are you sure you want to delete?")
    
    if (result) {
        document.getElementById('submit-btn').click();
    }
}