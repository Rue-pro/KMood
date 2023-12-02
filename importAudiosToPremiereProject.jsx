var SPEECH = "C:/Dev/YouTube Automation/KMood/ATEEZ_Yunho";
var BACKGROUND_SOUND =
  "C:/Dev/YouTube Automation/KMood/Assets/background_sound.mp3";
var speechFolder = null;
$.writeln(app.project);
app.project.importFiles(SPEECH, true, app.project.rootItem);

// app.project.importFiles(BACKGROUND_SOUND, true, app.project.rootItem);

for (var i = 0; i < app.project.rootItem.children.length; i++) {
  $.writeln("import: " + app.project.rootItem.children[i].name);

  if (app.project.rootItem.children[i].name === "audios") {
    speechFolder = app.project.rootItem.children[i];
  }
  /*if (app.project.rootItem.children[i].name === "background_sound.mp3") {
    $.vars.backgroundSound = app.project.rootItem.children[i];
  }*/
}

// app.project.sequences[0].audioTracks[1].insertClip(
//   $.vars.backgroundSound,
//   app.project.sequences[0].end
// );

function bubbleSort(coll) {
  var stepsCount = coll.length - 1;
  var swapped;
  do {
    swapped = false;
    for (var i = 0; i < stepsCount; i += 1) {
      currentNumber = parseInt(coll[i].name);
      nextNumber = parseInt(coll[i + 1].name);
      if (currentNumber > nextNumber) {
        var temp = coll[i];
        coll[i] = coll[i + 1];
        coll[i + 1] = temp;
        swapped = true;
      }
    }
    stepsCount -= 1;
  } while (swapped);

  return coll;
}

$.writeln("sequence: " + app.project.sequences[0].name);

var audiosToUpload = [];
for (var j = 0; j < speechFolder.children.length; j++) {
  audiosToUpload.push(speechFolder.children[j]);
}
audiosToUpload = bubbleSort(audiosToUpload);

$.writeln("sequence duration: " + app.project.sequences[0].end);

for (var j = 0; j < audiosToUpload.length; j++) {
  result = app.project.sequences[0].audioTracks[0].insertClip(
    audiosToUpload[j],
    app.project.sequences[0].end
  );
}
