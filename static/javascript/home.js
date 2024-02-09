

// função para o esquema de mudança dos botões do menu lateral abaixo da foto
$(document).ready(function(){
    var activeButton = null;
  
    $("#escolha_formulario_senha, #btn_mudar_capa, #btn_amigos, #btn_apostila, #btn_mudar_tema ").click(function(){
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
  
      if (clickedId === activeButton) {
        // Se o botão ativo for clicado novamente, mostre o feed e redefina o texto do botão
        $("#feed").show();
        $("#" + targetDivId).hide();
        $(this).text(
          clickedId === 'escolha_formulario_senha' ? "Mudar senha" : 
          clickedId === 'btn_mudar_capa' ? "Mudar foto de capa" : 
          activeButton === 'btn_amigos' ? "Amigos" :
          activeButton === 'btn_mudar_tema' ? 'Mudar Tema' : 'apostilas' );
        activeButton = null;
      } else {
        // Esconda todas as divs
        $("#feed, #mudar_senha, #mudar_capa, #amigos, #apostilas , #mudar_tema").hide();
  
        // Mostre a div correspondente ao botão clicado
        $("#" + targetDivId).show();
        $(this).text(buttonText);
  
        // Redefina o texto do botão ativo anterior
        if (activeButton) {
          $("#" + activeButton).text(
            activeButton === 'escolha_formulario_senha' ? "Mudar senha" : 
            activeButton === 'btn_mudar_capa' ? "Mudar foto de capa" : 
            activeButton === 'btn_amigos' ? "Amigos" : 
            activeButton === 'btn_mudar_tema' ? 'Mudar Tema' : 'apostilas' );
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
        <form action="/enviarFoto" enctype="multipart/form-data" method="post">
            <input type="file" name="foto" id="foto">
            <input type="hidden" name="emailUsuario" value="{{ email }}">
            <input type="hidden" name="rota" value="/cliente">
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