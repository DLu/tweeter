function clear_node(node_name)
{
  var node = document.getElementById(node_name);
  while (node.hasChildNodes()) {
    node.removeChild(node.lastChild);
  }
  return node;
}

function load_from_twitter(id, element, error)
{
  var o = $.getJSON("https://api.twitter.com/1/statuses/oembed.json?id=" + id + "&align=left&callback=?",
    function(data){ $(element).html(data.html);});
  if(error)
    o.error(error);
}

function load_tweet(id, retweeter, id2)
{
  if(id){
    load_from_twitter(id, '#tweet',
    function(a,b,c){
      $.getJSON("/formatted", function(data){ $('#tweet').html(data.html) });
    });
  }else{
    clear_node('tweet');
  }
  if(retweeter){
    $('#rt').html('@' + retweeter + ' retweeted');
  }else{
    clear_node('rt');
  }
  if(id2){
    load_from_twitter(id2, '#tweet2');
  }else{
    clear_node('tweet2');
  }
}

function load_img(extra_img)
{
    var img = document.getElementById('tweet_img');
    if(extra_img){
        img.setAttribute('src', extra_img);
    }else{
        img.setAttribute('src', '');
    }
}
function update(){
  $.getJSON("/update",
    function(data){
      $('#status').html(data.message);
      load_page();
      });
}

function save_to_disk(){
  $.getJSON("/write",
    function(data){
      $('#status').html(data.message);
      });
}

function clear_progress(){
  $.getJSON("/clear",
    function(data){
      $('#status').html(data.message);
      load_page();
      });
}
