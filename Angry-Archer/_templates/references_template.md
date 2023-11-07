<%*
  function getKeyByValue(map, val) {
    for (const [key, value] of map.entries()) {
      for (const element of value) {
        if (val === element) {
          return key;
        }
      }
    }
  }

  function iterateOverMap(map, array) {
    for (const [key, value] of map.entries()) {
      for (const val of value) {
        array.push(val);
      }
    }
  }
  
  function createParameterListFromMap(map, list) {
    for (const [key, value] of map.entries()) {
      let paramPrintOut;
      paramPrintOut = `**${key}:**`;
      paramPrintOut = paramPrintOut.concat(` ${value.map(file => `[[${file}]]`).join(`, `)}`);
      paramsList.push(paramPrintOut);
    }
  }

  function getFilesInFolder(folder, query = '', ext = ['md', 'txt']) {
    let filesInFolder;
    filesInFolder = app.vault.getFiles()
      .filter(file=>file.path.includes(folder))
      .filter(tFile=>ext.includes(tFile.extension))
      .filter(tFile=>tFile.basename.toLowerCase().includes(query.toLowerCase()))
      .map(tFile=>tFile.basename);
    if (filesInFolder.length == 0) {
      filesInFolder = [];
    }
    return filesInFolder;
  }

  async function createSingleSelectMenuDialog(menuOptions, menuPlaceholder) {
    const selectedOption = [];
    selectedOption.push(await tp.system.suggester(menuOptions, menuOptions, false, menuPlaceholder));
    return selectedOption;
  }

  async function createMultiSelectMenuDialog(menuOptions, menuPlaceholder) {   
    const selectedOptions = []; 
    while (true) {
      let updatedMenuPlaceholder = '';
      if (selectedOptions.length >= 1) {
        updatedMenuPlaceholder = `${menuPlaceholder} ${selectedOptions.map(file => file).join(`, `)}`;
      } else {
        updatedMenuPlaceholder = menuPlaceholder;
      }
      const selectedOption = await createSingleSelectMenuDialog(menuOptions, updatedMenuPlaceholder);
      if (!selectedOption) {
        break;
      } else {
        selectedOptions.push(selectedOption);
        menuOptions.splice(menuOptions.indexOf(selectedOption), 1);
      }
    }
    return selectedOptions;
  }

  async function createSingleSelectMenuFromFiles(folder, menuPlaceholder) {
    const filesInFolder = getFilesInFolder(folder);
    return await createSingleSelectMenuDialog(filesInFolder, menuPlaceholder);
  }

  async function createMultiSelectMenuFromFiles(folder, menuPlaceholder) {
    const filesInFolder = getFilesInFolder(folder);
    return await createMultiSelectMenuDialog(filesInFolder, menuPlaceholder);
  }    
-%>
<%*
  // User prompt for type of reference
  const referenceTypes = new Map();
  referenceTypes.set("Audio", ["Music", "SFX"]);
  referenceTypes.set("Image", ["Artwork", "Figure Study"]);
  referenceTypes.set("Video", ["Motion Graphics", "Short Film", "Title Sequence", "Misc. Video"]);
  const referenceTypesList = [];
  iterateOverMap(referenceTypes, referenceTypesList);
  const referenceType = await tp.system.suggester(referenceTypesList, referenceTypesList,
    false, "Select the type of reference: ");
  const mediaType = getKeyByValue(referenceTypes, referenceType);
-%>
<%*
  // tags
  const tag = referenceType
    .toLowerCase()
    .replace(/\bmisc\. /g, '')
    .replace(/[./\\?%*:|"<>]/g, '')
    .replace(/ /g, '-');
-%>
<%*
  // URL
  const url = await tp.system.prompt(`Enter the URL for the ${referenceType.toLowerCase()}:`);
-%>
<%*
  // Frontmatter
  const frontMatter = `---\ntags:\n  - reference\n  - ${tag}\nsource: ${url}\n---`;
-%>
<%*
  // Image Parameters
  // TODO: if 'paramFolder' is empty, then the select is not from files and instead from a given list? 
  const paramMap = new Map();
  paramMap.set('Title', {'promptType': 'text input', 'paramFolder': '', 'selectedOptions': []});
  paramMap.set('Date', {'promptType': 'text input', 'paramFolder': '', 'selectedOptions': []});
  paramMap.set('Location', {'promptType': 'text input', 'paramFolder': '', 'selectedOptions': []});
  paramMap.set('Dimensions', {'promptType': 'text input', 'paramFolder': '', 'selectedOptions': []});
  
  paramMap.set('Artist', {'promptType': 'single select', 'paramFolder': 'temp/art style/', 'selectedOptions': []});

  paramMap.set('Style', {'promptType': 'multi select', 'paramFolder': 'temp/art style/', 'selectedOptions': []});
  paramMap.set('Art Period', {'promptType': 'multi select', 'paramFolder': 'temp/art period/', 'selectedOptions': []});
  paramMap.set('Subject Matter', {'promptType': 'multi select', 'paramFolder': 'temp/art period/', 'selectedOptions': []});
  paramMap.set('Media', {'promptType': 'multi select', 'paramFolder': 'temp/art period/', 'selectedOptions': []});
  paramMap.set('Vibes', {'promptType': 'multi select', 'paramFolder': 'temp/art period/', 'selectedOptions': []});
  let params = ['Title', 'Artist', 'Date', 'Style', 'Art Period', 'Genre / Subject Matter', 'Media', 'Location', 'Dimensions', 'Vibes'];
-%>
<%*
  // Video Parameters
  let defaultParams = [];
  let params = [];
  let paramsList = [];
  let selectedParamChoices = new Map();

  if (referenceType == "Motion Graphics" || referenceType == "Title Sequence") {
    defaultParams = ['Design and Animation', 'Music and SFX', 'Vibes'];
    if (referenceType === 'Motion Graphics') {
      params = params.concat('Brands', defaultParams);
    }
    if (referenceType === 'Title Sequence') {
      params = params.concat('Movie and TV', defaultParams);
    }
  }
  
  // Multi-select
  for (const param of params) {
    const paramFolder = `${param}/`;
    const menuPlaceholder = `'${param}' parameter. Press [ESC] to proceed.`;
    const selectedOptions = await createSingleSelectMenuFromFiles(paramFolder, menuPlaceholder);
    selectedParamChoices.set(param, selectedOptions);
    console.log(selectedParamChoices)
  }
  createParameterListFromMap(selectedParamChoices, paramsList);
-%>
<% frontMatter %>
## <% mediaType %>

<% paramsList.map(item => `${item}`).join(`\n`) %>