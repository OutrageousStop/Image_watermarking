var fileTag = document.getElementById("original_image"),
    preview = document.getElementById("original_preview"),
    waterTag = document.getElementById("watermark_image"),
    waterpreview = document.getElementById("watermark_preview");

fileTag.addEventListener("change", function() {
  changeImage(this, preview);
});

waterTag.addEventListener("change", function() {
  changeImage(this, waterpreview);
})


function changeImage(input, preview) {
  var reader;

  if (input.files && input.files[0]) {
    reader = new FileReader();

    reader.onload = function(e) {
      preview.setAttribute('src', e.target.result);
      preview.setAttribute("widght", 200);
      preview.setAttribute("height", 200);
    }
    reader.readAsDataURL(input.files[0]);
  }
}