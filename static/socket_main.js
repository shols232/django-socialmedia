    var updatedRoomName = ''
    if (roomName != ''){} 
    var loc = window.location
    var wsStart = "ws://"
    if (loc.protocol == "https:"){
        wsStart = "wss://"
    }
    var chatSocket = new ReconnectingWebSocket(
        wsStart + window.location.host +
        '/ws/chat/' + roomName + '/');

    chatSocket.onopen = function(e) {
      console.log('na from here')
      fetchMessages(roomName);
    }

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        if (data['command'] === 'messages') {
          if(data['status'] === 'Chat with that id does not exist'){
            console.log(data["status"])
            window.location.replace(window.location.origin + `/chat/`)
          }else{
            if (window.innerWidth < 740){
              console.log('000000000000000000000000000000000000000000000001111111111')
              document.getElementById('sidepanel').style.display = 'none'
              document.querySelector('.content').style.display = 'block'
            }
            for (let i=0; i<data['messages'].length; i++) {
              createMessage(data['messages'][i]);
            }
          }
        } else if (data['command'] === 'new_message'){
          
          var prom = new Promise(function(resolve, error){
            createMessage(data['message'])
            resolve("123")
          })
          prom
          .then(function(){
            var chatId = updatedRoomName === '' ? roomName : updatedRoomName
          var li = document.getElementById(`chat-${chatId}`)
          var ul = document.getElementById("contacts-ul")
          var firstUl = ul.querySelectorAll("li")[0]
          var parag = li.getElementsByClassName("preview")[0]
          parag.innerHTML = data["message"].content
          ul.insertBefore(li, firstUl)
          })
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
      console.log('ohio')
        var messageInputDom = document.getElementById('chat-message-input');
        // var regex = /^\s*(?:<br\s*\/?\s*>)+|(?:<br\s*\/?\s*>)+\s*$/gi
        // var holla = 
        // messageInputDom.innerText = messageInputDom.innerText.trim()
        var message = messageInputDom.innerHTML.replace(/(<div><br><\/div>)$/m,"");
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'message': message,
            // 'from': username,
            'chatID':updatedRoomName === '' ? roomName : updatedRoomName
        }));
        messageInputDom.innerText = '';
      };

    function fetchMessages(id) {
      console.log(id)
      console.log(roomName)
      chatSocket.send(JSON.stringify({'command': 'fetch_messages' , 'jum':'jum', 'id':id}));
    }

    function formatTime(data){
      var newDate = new Date(data.date_posted).getMinutes().toString()
      console.log(newDate.length)
      
      if ( newDate.length > 1 ){
        return newDate
      }else{
        return '0'+ newDate
      }
    }

    function createMessage(data) {
      var author = data['author'];
      var msgListTag = document.createElement('li');
      var newDiv = document.createElement('div');
      var imgTag = document.createElement('img');
      var pTag = document.createElement('p');
      var autPtag = document.createElement('span')
      var smallTag = document.createElement('small');
      smallTag.className = 'date-posted'
      smallTag.textContent =  new Date(data.date_posted).getHours() + ':' + formatTime(data)
      pTag.innerHTML = data.content
      newDiv.className ='msg-div'
      autPtag.textContent = author

      imgTag.src = data.image_url;
      
      if (author === username) {
        console.log(author, username)
        msgListTag.className = 'replies';
        smallTag.className = 'reply-date';
        autPtag.className = 'chat-author'
      } else {
        msgListTag.className = 'sent';
        smallTag.className = 'reply-date-replier'
      }
      msgListTag.appendChild(autPtag)
      newDiv.appendChild(imgTag)
      newDiv.appendChild(pTag);
      msgListTag.appendChild(newDiv)
      msgListTag.appendChild(smallTag)

      document.querySelector('#chat-log').appendChild(msgListTag);
      
      
      document.querySelector(".messages").scrollTop = document.querySelector('.messages').scrollHeight
    };
    var contact = document.querySelectorAll('.contact')
    contact.forEach(item => {
      item.addEventListener('click', function(e){
      console.log('aleeyyyyyoopppppppppppppppppp222222222222222')
      $.get(`/chat/${item.dataset.chatid}/`, function(data, status){
        if (status == "success"){    
          console.log('aleeyyyyyoopppppppppppppppppp111113333333111')
          history.pushState({
            id: 'homepage'
          }, 'Chat | something', `/chat/${item.dataset.chatid}`);
          document.getElementById('chat-log').innerHTML = ''
          // chatSocket.onopen
          updatedRoomName = item.dataset.chatid
          // fetchMessages(item.dataset.chatid)
          chatSocket.onopen = function(e) {
            
            fetchMessages(item.dataset.chatid);
          }
          chatSocket.refresh()
        }
          
      });

    })
    });


    window.onload = function(){
      document.querySelector(".messages").scrollTop = document.querySelector('.messages').scrollHeight
    }
