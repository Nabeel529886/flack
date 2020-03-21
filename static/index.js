document.addEventListener("DOMContentLoaded", () => {

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on("connect", () => {

    document.querySelector("#button").onclick = () => {
      const msg = document.querySelector("#message").value;
      socket.emit("msg sent", {"message": msg});
    };
  });

socket.on("msg recieve", (msg) => {
  const li = document.createElement("li");
  li.innerHTML = msg.message;
  document.querySelector("#messages").append(li);
});
});
