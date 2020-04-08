document.addEventListener("DOMContentLoaded", () => {

  var username = document.querySelector("#get_username").innerHTML;

  document.querySelector('#show-sidebar-button').onclick = () => {
      document.querySelector('#sidebar').classList.toggle('view-sidebar');
  };

  let msg = document.getElementById("message");
  msg.addEventListener("keyup", function(event) {
      event.preventDefault();
      if (event.keyCode === 13) {
          document.getElementById("submit").click();
      }
  });

  var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port)

  let room = "Electromates"
  joinRoom("Electromates")
  const submit_btn = document.querySelector("#submit");
  submit_btn.addEventListener("click", (e) => {

    const msg = document.querySelector("#message").value;
    socket.emit("incoming-msg", {"msg": msg, "username": username, "room": room})
    document.querySelector("#message").value = "";
    document.querySelector("#message").focus();
  });

  socket.on('message', data => {

    if (data.msg){
      const p = document.createElement("p");
      const span_username = document.createElement("span");
      const span_timestamp = document.createElement("timestamp");
      const br = document.createElement("br");

      if (data.username == username){
        p.setAttribute("class", "my-msg");
        // Username
        span_username.setAttribute("class", "my-name");
        span_username.innerText = data.name;

        // Timestamp
        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = data.time_stamp;

        // HTML to append
        p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

        //Append
        document.querySelector('#display-message-section').append(p);
      }
      else if (typeof data.username !== 'undefined') {
          p.setAttribute("class", "others-msg");
          // Username
          span_username.setAttribute("class", "other-name");
          span_username.innerText = data.name;

          // Timestamp
          span_timestamp.setAttribute("class", "timestamp");
          span_timestamp.innerText = data.time_stamp;

          // HTML to append
          p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

          //Append
          document.querySelector('#display-message-section').append(p);
      }
      else{
        printSysMsg(data.msg);
      }
      scrollDownChatWindow();
    }
          });
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML
            // Check if user already in the room
            if (newRoom === room) {
                msg = `You are already in ${room} room.`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        };
    });

    function joinRoom(room) {

        // Join room
        socket.emit('join', {'username': username, 'room': room});

        // Highlight selected room
        document.querySelector('#' + CSS.escape(room)).style.color = "white";
        document.querySelector('#' + CSS.escape(room)).style.border = "2px solid #777";
        document.querySelector('#' + CSS.escape(room)).style.borderRight = "4px solid #777";
        document.querySelector('#' + CSS.escape(room)).style.borderRadius = "25px";
        document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "#999";

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Autofocus on text box
        document.querySelector("#message").focus();
    }

    function leaveRoom(room){
      socket.emit('leave', {'username': username, "room": room})
      document.querySelectorAll('.select-room').forEach(p => {
          p.style.color = "black";
          p.style.border = "none";
          p.style.backgroundColor = "white";

      });
    }

    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#message").focus();
    }
});
