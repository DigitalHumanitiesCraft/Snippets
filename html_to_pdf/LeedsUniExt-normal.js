﻿import { jsPDF } from "jspdf"
var callAddFont = function () {
this.addFileToVFS('LeedsUniExt-normal.ttf', font);
this.addFont('LeedsUniExt-normal.ttf', 'LeedsUniExt', 'normal');
};
jsPDF.API.events.push(['addFonts', callAddFont])