  import { EmojiButton } from "https://cdn.jsdelivr.net/npm/@joeattardi/emoji-button@4.0.2/dist/index.min.js";
  var picker = new EmojiButton();
  const trigger = document.querySelector('.trigger');

  picker.on('emoji', selection => {
    console.log(selection.emoji)
  });
  console.log(picker)
trigger.addEventListener('click', function(picker){
  picker.togglePicker(trigger)
});

