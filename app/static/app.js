(function(){
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const convertBtn = document.getElementById('convertBtn');
  const clearBtn = document.getElementById('clearBtn');
  const fileInfo = document.getElementById('fileInfo');
  const progressWrap = document.getElementById('progressWrap');
  const progressBar = document.getElementById('progressBar');
  const progressLabel = document.getElementById('progressLabel');
  const statusLabel = document.getElementById('statusLabel');

  let selectedFile = null;

  function fmtBytes(bytes){
    if(bytes === 0) return '0 B';
    const k = 1024, sizes = ['B','KB','MB','GB','TB'];
    const i = Math.floor(Math.max(0, Math.log(bytes)/Math.log(k)));
    const val = bytes / Math.pow(k, i);
    return `${val.toFixed(val >= 100 ? 0 : val >= 10 ? 1 : 2)} ${sizes[i]}`;
  }

  function setFile(file){
    selectedFile = file;
    if(file){
      fileInfo.classList.remove('hidden');
      fileInfo.textContent = `${file.name} • ${fmtBytes(file.size)}`;
      convertBtn.disabled = false;
      clearBtn.disabled = false;
    } else {
      fileInfo.classList.add('hidden');
      convertBtn.disabled = true;
      clearBtn.disabled = true;
    }
  }

  function blobToBase64(blob){
    return new Promise((resolve, reject)=>{
      const reader = new FileReader();
      reader.onloadend = ()=> resolve(reader.result.split(',')[1]);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  async function saveBlob(blob, filename){
    const nativeApi = window.pywebview && window.pywebview.api && window.pywebview.api.save_file;

    if(nativeApi){
      try{
        const base64 = await blobToBase64(blob);
        const result = await window.pywebview.api.save_file(filename, base64);
        if(result && result.ok){
          statusLabel.textContent = 'Arquivo salvo com sucesso.';
        } else if(result && result.error){
          statusLabel.textContent = 'Falha ao salvar.';
          alert('Falha ao salvar arquivo: ' + result.error);
        } else {
          statusLabel.textContent = 'Cancelado.';
        }
      }catch(err){
        statusLabel.textContent = 'Falha ao salvar.';
        alert('Falha ao salvar o arquivo.');
      }
      return;
    }

    // Fallback (navegador comum / modo Docker): download via blob-URL
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(()=> URL.revokeObjectURL(url), 0);
    statusLabel.textContent = 'Concluído';
  }

  function resetProgress(){
    progressBar.style.width = '0%';
    progressLabel.textContent = '0%';
    statusLabel.textContent = '';
    progressWrap.classList.add('hidden');
  }

  function startUpload(){
    if(!selectedFile){ return; }
    if(!selectedFile.name.toLowerCase().endsWith('.dbc')){
      alert('Selecione um arquivo com extensão .dbc');
      return;
    }

    progressWrap.classList.remove('hidden');
    progressBar.style.width = '0%';
    progressLabel.textContent = '0%';
    statusLabel.textContent = 'Enviando…';
    convertBtn.disabled = true;

    const form = new FormData();
    form.append('file', selectedFile, selectedFile.name);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/convert');
    xhr.responseType = 'blob';

    xhr.upload.onprogress = (e)=>{
      if(e.lengthComputable){
        const pct = Math.round((e.loaded / e.total) * 100);
        progressBar.style.width = pct + '%';
        progressLabel.textContent = pct + '%';
      }
    };

    xhr.onreadystatechange = ()=>{
      if(xhr.readyState === XMLHttpRequest.HEADERS_RECEIVED){
        statusLabel.textContent = 'Convertendo…';
      }
    };

    xhr.onload = ()=>{
      if(xhr.status >= 200 && xhr.status < 300){
        progressBar.style.width = '100%';
        progressLabel.textContent = '100%';
        statusLabel.textContent = 'Gerando arquivo…';

        const blob = xhr.response;
        const disposition = xhr.getResponseHeader('Content-Disposition') || '';
        let filename = 'convertido.xlsx';
        const match = disposition.match(/filename="?([^";]+)"?/i);
        if(match && match[1]){ filename = match[1]; }

        saveBlob(blob, filename).finally(()=>{ convertBtn.disabled = false; });
      } else {
        let errorMessage = 'Falha na conversão';
        try{
          const reader = new FileReader();
          reader.onload = ()=>{
            try{
              const data = JSON.parse(reader.result);
              alert(data.detail || errorMessage);
            }catch{ alert(errorMessage); }
          };
          reader.readAsText(xhr.response);
        }catch{ alert(errorMessage); }
        convertBtn.disabled = false;
      }
    };

    xhr.onerror = ()=>{
      alert('Erro de rede. Tente novamente.');
      convertBtn.disabled = false;
    };

    xhr.send(form);
  }

  // Drag and drop
  ['dragenter','dragover'].forEach(evt=>{
    dropzone.addEventListener(evt, (e)=>{
      e.preventDefault(); e.stopPropagation();
      dropzone.classList.add('hover');
    });
  });
  ['dragleave','drop'].forEach(evt=>{
    dropzone.addEventListener(evt, (e)=>{
      e.preventDefault(); e.stopPropagation();
      dropzone.classList.remove('hover');
    });
  });
  dropzone.addEventListener('drop', (e)=>{
    const files = e.dataTransfer.files;
    if(files && files[0]) setFile(files[0]);
  });

  // Click to open file dialog
  dropzone.addEventListener('click', ()=> fileInput.click());
  dropzone.addEventListener('keypress', (e)=>{ if(e.key === 'Enter' || e.key === ' '){ fileInput.click(); }});

  fileInput.addEventListener('change', ()=>{
    setFile(fileInput.files && fileInput.files[0] ? fileInput.files[0] : null);
    resetProgress();
  });

  convertBtn.addEventListener('click', startUpload);
  clearBtn.addEventListener('click', ()=>{ setFile(null); resetProgress(); fileInput.value = ''; });
})();


