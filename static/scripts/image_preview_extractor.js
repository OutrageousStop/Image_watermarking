var imgTag = document.getElementById("image"),
    preview = document.getElementById('image_preview');

imgTag.addEventListener("change", function() {
    changeImage(this, preview);
});

function changeImage(input, preview){
    var reader;
    if (input.files && input.files[0])
    {
        reader = new FileReader();
        reader.onload = function(e) {
            preview.setAttribute('src', e.target.result);
            preview.setAttribute('width', 200);
            preview.setAttribute('height', 200);
        }
        reader.readAsDataURL(input.files[0]);
    }
}