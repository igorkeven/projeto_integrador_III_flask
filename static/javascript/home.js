
$(document).ready(function() {
  $(".topo").click(function() {
    $("html, body").animate(
      {
        scrollTop: 0
      },
      100 // Tempo em milissegundos para a animação
    );
  });
});

window.addEventListener('scroll', function() {
  // Calcula a opacidade com base na posição de rolagem
  var opacity = 1 - Math.min(window.scrollY / 350, 1);
  
  // Aplica a opacidade ao elemento
  document.querySelector('#formDesafio').style.opacity = opacity.toString();
  
  // Altera a altura do elemento com base na opacidade
  if (opacity <= 0) {
    document.querySelector('#formDesafio').style.height = '10px';
    document.querySelector('#formDesafio').style.display = 'none';
    document.querySelector('.topo').style.display = 'block';
  } else {
    document.querySelector('#formDesafio').style.height = 'auto';
    document.querySelector('.topo').style.display = 'none';
    document.querySelector('#formDesafio').style.display = 'block';
  }
});



// função para o esquema de mudança dos botões do menu lateral abaixo da foto
$(document).ready(function(){
    var activeButton = null;
  
    $("#escolha_formulario_senha, #btn_meus_desafios, #btn_desafios_concluidos, #btn_mudar_capa, #btn_amigos, #btn_apostila, #btn_mudar_tema, #btn_apagar_conta, #btn_mensagens, #btn_voltarConfig1, #btn_voltarConfig2 ").click(function(){
      var clickedId = $(this).attr('id');
      var targetDivId;
      var buttonText;
  
      if (clickedId === 'escolha_formulario_senha') {
        targetDivId = 'mudar_senha';
        buttonText = "Feed";
      } else if (clickedId === 'btn_mudar_capa') {
        targetDivId = 'mudar_capa';
        buttonText = "Feed";
      } else if (clickedId === 'btn_amigos') {
        targetDivId = 'amigos';
        buttonText = "Feed";
      } else if (clickedId === 'btn_apostila'){
        targetDivId = 'apostilas';
        buttonText = "Feed"; 
      } else if (clickedId === 'btn_mudar_tema'){
        targetDivId = 'mudar_tema';
        buttonText = "Feed";
      }
       else if (clickedId === 'btn_apagar_conta'){
        targetDivId = 'apagar_conta';
        buttonText = "Feed";
      }
       else if (clickedId === 'btn_mensagens'){
        targetDivId = 'mensagens';
        buttonText = "Feed";

      } else if (clickedId === 'btn_desafios_concluidos') {
        targetDivId = 'desafios_concluidos';
        buttonText = "feed";
      } else if (clickedId === 'btn_meus_desafios') {
        targetDivId = 'meus_desafios';
        buttonText ='feed';
     } else if (clickedId === 'btn_voltarConfig1' || clickedId === 'btn_voltarConfig2') {
     
         targetDivId = 'feed';
         buttonText = "Voltar";
        
       }
  
      if (clickedId === activeButton) {
        // Se o botão ativo for clicado novamente, mostre o feed e redefina o texto do botão
        $("#feed").show();
        if( targetDivId !== 'feed'){
        $("#" + targetDivId).hide();
        }
        $(this).text(
          clickedId === 'escolha_formulario_senha' ? "Mudar senha" : 
          clickedId === 'btn_mudar_capa' ? "Mudar foto de capa" : 
          clickedId === 'btn_amigos' ? "Amigos" :
          clickedId === 'btn_mudar_tema' ? 'Mudar Tema' :
          clickedId === 'btn_apagar_conta' ? 'Apagar conta':
          clickedId === 'btn_mensagens' ? 'Mensagens':
          clickedId === 'btn_desafios_concluidos' ? 'Desafios concluidos' :
          clickedId === 'btn_meus_desafios' ? 'Meus desafios':
          clickedId === 'btn_voltarConfig1' ? 'Voltar' :
          clickedId === 'btn_voltarConfig2' ? 'Voltar' :
          clickedId === 'btn_apostila' ?
          'apostilas' : 'Voltar');
        activeButton = null;
      } else {
// Esconda todas as divs
  $("#feed, #mudar_senha, #mudar_capa, #amigos, #apostilas , #mudar_tema, #apagar_conta, #mensagens , #desafios_concluidos, #meus_desafios").hide();      

        
          
        // Mostre a div correspondente ao botão clicado
        $("#" + targetDivId).show();
        $(this).text(buttonText);
      
       
  
        // Redefina o texto do botão ativo anterior
        if (activeButton) {
          $("#" + activeButton).text(
            activeButton === 'escolha_formulario_senha' ? "Mudar senha" : 
            activeButton === 'btn_mudar_capa' ? "Mudar foto de capa" : 
            activeButton === 'btn_amigos' ? "Amigos" : 
            activeButton === 'btn_mudar_tema' ? 'Mudar Tema' :
            activeButton === 'btn_apagar_conta' ? 'Apagar conta':
            activeButton === 'btn_mensagens' ? 'Mensagens':
            activeButton === 'btn_desafios_concluidos' ? 'Desafios concluidos' :
            activeButton === 'btn_meus_desafios' ? 'Meus desafios':
            activeButton === 'btn_voltarConfig1' ? 'Voltar' :
            activeButton === 'btn_voltarConfig2' ? 'Voltar' :
            activeButton === 'btn_apostila' ? 'apostilas' :
             'Voltar');
             
        }
  
        activeButton = clickedId;
      }
    });
  });


  



  //------------------------------------------------------------------------

  // esquema para quando clicar no botão configurações -------------------

  const btnConfig = document.getElementById('btn_config');
  const btnVoltarConfg = document.querySelectorAll('.btn_voltarConfig');
  const btn_desafios = document.getElementById('btn_desafios');
  const menuLateralEsquerdo1 = document.getElementsByClassName('menu_lateral_esquendo_1')[0];
  const menuLateralEsquerdo2 = document.getElementsByClassName('menu_lateral_esquendo_2')[0];
  const menuLateralEsquerdo3 = document.getElementsByClassName('menu_lateral_esquendo_3')[0];
  btnConfig.addEventListener('click', function() {
    
    menuLateralEsquerdo1.style.display = 'none';
    menuLateralEsquerdo2.style.display = 'block';
  });

  btn_desafios.addEventListener('click', function(){
    menuLateralEsquerdo1.style.display = 'none';
    menuLateralEsquerdo3.style.display = 'block';
  })

  btnVoltarConfg.forEach(btn => {
    btn.addEventListener('click', function(){
      menuLateralEsquerdo1.style.display = 'block';
      menuLateralEsquerdo2.style.display = 'none';
      menuLateralEsquerdo3.style.display = 'none';
      
    })
  });


  // --------- area do modal para envio de foto do perfil --------------

  document.getElementById("foto_perfi").addEventListener("click", function() {
              
    if (this.src.includes("user.png")) {
      
        // usuário ainda não tem uma imagem definida, permitir o envio da foto!
        
    }else{
        // usuario ja tem uma foto, solicitar confirmação de mudança
        if (confirm("Você tem certeza que deseja mudar sua foto?")) {
            // usuario confirmou , pode enviar nova foto
            
        }else{
            // usuario cancelou a mudança da foto
            return;
        }
    }

    var modal = document.createElement("div");
    modal.classList.add("modal");
    modal.innerHTML = `
    <div class="modal-content">
        <span class="close">&times;</span>
        <form action="/enviar_foto_perfil" enctype="multipart/form-data" method="post">
            <input type="file" name="foto" id="foto">
           
            
            <input type="submit" value="Enviar">
        </form>

    </div>
    
    `;
    document.body.appendChild(modal);
   
    var BotaoFechar = modal.querySelector(".close");
    BotaoFechar.addEventListener("click", ()=>{
        modal.remove();
    })
});

//------------------------------------------------------------------------------------