from flask import Flask, render_template, request, session, make_response
import pdfkit
from reportlab.rl_config import defaultPageSize
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
import math
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Spacer


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/download1", methods = ["POST"])
def sweaterpdf():
    rpi = session['rpi']
    castOn = session['castOn']
    bustCount = session['bustCount']
    fbNeckCount = session['fbNeckCount']
    sleeveNeckCount = session['sleeveNeckCount']
    yokeIncRows = session['yokeIncRows']
    bottomYokeCount = session['bottomYokeCount']
    upperBack = session['upperBack']
    lowerTorso = session['lowerTorso']
    upperTorso = session['upperTorso']
    units = session['units']
    sleeveYokeEndCount = session['sleeveYokeEndCount']
    fbYokeEndCount = session['fbYokeEndCount']
    sleeveCO = session['sleeveCO']
    waistDecs = session['waistDecs']
    waistDecRows = session['waistDecRows']
    waistCount = session['waistCount']
    hipIncs = session['hipIncs']
    hipIncRows = session['hipIncRows']
    bottomCount = session['bottomCount']
    topSleeveCount = session['topSleeveCount']
    sleeveDecs = session['sleeveDecs']
    sleeveDecRows = session['sleeveDecRows']
    bottomSleeveCount = session['bottomSleeveCount']
    tAnswer = session['tAnswer']
    sAnswer = session['sAnswer']

    #Pattern PDF output
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    spacer = Spacer(0,0.25*inch)
    page_height=defaultPageSize[1]
    page_width=defaultPageSize[0]
    pattern = []
    #Paragraphs for knitting pattern
    pattern.append(Paragraph("Stitch Abbreviation guide", styleN))
    pattern.append(Paragraph("<b>-k1:</b> Knit one", styleN))
    pattern.append(Paragraph("<b>-m1:</b> Make one", styleN))
    pattern.append(Paragraph("<b>-k2tog:</b> Knit 2 together", styleN))
    pattern.append(Paragraph("<b>-sl:</b> slip (slip marker from left to right needle)", styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Cast on {castOn} stitches to circular needles and join in the round. Place marker for beginning of round. Knit {fbNeckCount/2},place marker, knit {sleeveNeckCount}, place marker, knit {fbNeckCount}, place marker, knit to end of round. ({fbNeckCount} stitches for front and back, {sleeveNeckCount} stitches for each sleeve)", styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Knit 2 rounds even. On next round, begin yoke increases as follows: knit to 1 stitch before marker. m1, k1, slip marker, k1, m1, knit to 1 stitch before next marker. Continue like this until end of round (do not m1 before or after end of round marker). 8 stitches increased. Increase every other row {yokeIncRows-1} times until you have {bottomYokeCount} stitches. Continue even without increasing until {upperBack} {units} or desired length to bottom of armpit is reached.", styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Divide for sleeves: knit to first marker. Remove marker (and all others as you go), and place next {sleeveYokeEndCount} stitches on holder for sleeve. Cast on {sleeveCO/2} stitches, place marker for side (this will be your new beginning of round). Cast on {sleeveCO/2} more stitches. Knit across next {fbYokeEndCount} stitches and remove marker. Place next {sleeveYokeEndCount} stitches on holder for 2nd sleeve. Cast on {sleeveCO/2} stitches. Place marker for 2nd side. Cast on {sleeveCO/2} more stitches. Knit to end of round ({bustCount} stitches).",styleN))
    pattern.append(spacer)
    if(sAnswer=="no"):
        pattern.append(Paragraph(f"Knit in the round for {(lowerTorso + upperTorso)} {units} or until desired length is reached. Bind off loosely.", styleN))
    else:
        if(tAnswer=="hourglass"):
            pattern.append(Paragraph(f"Knit 2 rows in the round, then begin waist decreases as follows: *k1, k2tog, knit to 3 stitches before side marker, k2tog, k, sl marker, repeat from *. Repeat decrease every {waistDecs} round {waistDecRows-1} more times ({waistCount} stitches). Knit {rpi} rows even. Begin hip increases as follows: *k1, m1, knit to 2 stitches before side marker, m1, k1, sl marker, repeat from *. Repeat increase every {hipIncs} round {hipIncRows-1} more times ({bottomCount} stitches). Knit until desired length is reached, bind off all stitches loosely.",styleN))
        else:
            if(bottomCount > bustCount):
                pattern.append(Paragraph(f"Knit 2 rows in the round, then begin shaping as follows: *k1, m1, knit to 2 stitches before side marker, m1, k1, sl marker, repeat from *. Repeat increase every {hipIncs} round {hipIncRows-1} more times ({bottomCount} stitches). Knit until desired length is reached, bind off all stitches loosely.",styleN))
            else:
                if(bottomCount < bustCount):
                    pattern.append(Paragraph(f"Knit 2 rows in the round, then begin shaping as follows: *k1, k2tog, knit to 3 stitches before side marker, k2tog, k1, sl marker, repeat from *. Repeat decrease every {waistDecs} round {waistDecRows-1} more times ({bottomCount} stitches). Knit until desired length is reached, bind off all stitches loosely.",styleN))
                else:
                    pattern.append(Paragraph(f"Knit in the round for {(lowerTorso + upperTorso)} {units} or until desired length is reached. Bind off loosely.", styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Knit sleeves: Place {sleeveYokeEndCount} stitches from holders onto small circulars or DPNs. Beginning in the center of underarm, pick up and knit {sleeveCO/2} stitches. Knit across {sleeveYokeEndCount} stitches. Pick up and knit {sleeveCO/2} more stitches. Place marker for beginning/end of round ({topSleeveCount} stitches). Knit even for 2 rounds. Begin sleeve shaping as follows: k1, k2tog, knit to 3 stitches before marker, k2tog, k1 (2 stitches decreased). Repeate decrease round every {sleeveDecs} rounds {sleeveDecRows-1} more times ({bottomSleeveCount} stitches). Knit even until desired length is reached, bind off all stitches loosely. Repeat these instructions for 2nd sleeve.", styleN))
    output = io.BytesIO()
    c = Canvas(output) #create pdf
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(page_width/2, page_height-60, "Basic Sweater Pattern") #title
    f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1) #frame for pattern
    f.addFromList(pattern,c) #put pattern in frame
    c.showPage()
    c.save()

    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename='Basic_Sweater_Pattern.pdf"
    response.mimetype = 'application/pdf'
    return response

@app.route("/download", methods =["POST"])
def sockpdf():
    castOn = session['castOn']
    heelFlapRows = session['heelFlapRows']
    heelTurnFirstRow = session['heelTurnFirstRow']
    heelTurnSts = session['heelTurnSts']
    finalHeelCount = session['finalHeelCount']
    gussetPU = session['gussetPU']
    gussetDecCount = session['gussetDecCount']
    footCount = session['footCount']
    footLength = session['footLength']
    units = session['units']
    toeLength = session['toeLength']
    toeDecCount = session['toeDecCount']
    toeCount = session['toeCount']
    cuffLength = session['cuffLength']
    heelFlap = session['heelFlap']

    #Pattern PDF output
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    spacer = Spacer(0,0.25*inch)
    page_height=defaultPageSize[1]
    page_width=defaultPageSize[0]
    pattern = []
    #Paragraphs for knitting pattern
    pattern.append(Paragraph("Stitch Abbreviation guide", styleN))
    pattern.append(Paragraph("<b>-k1:</b> Knit one", styleN))
    pattern.append(Paragraph("<b>-m1:</b> Make one", styleN))
    pattern.append(Paragraph("<b>-k2tog:</b> Knit 2 together", styleN))
    pattern.append(Paragraph("<b>-ssk:</b> Slip Slip Knit", styleN))
    pattern.append(Paragraph("<b>-sl:</b> slip 1 from left to right needle", styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Cast on {castOn} stitches and join in the round, being careful not to twist. Knit in the round in desired pattern for {round(cuffLength)} {units} or until cuff has reached desired length. Divide for heel flap: place last {heelFlap} stitches on hold for top of foot. Heel flap will be worked over remaining {heelFlap} stitches.",styleN))
    pattern.append(Paragraph("Row 1: *sl1, k1* repeat until end of round",styleN))
    pattern.append(Paragraph("Row 2: sl1, purl to end of round",styleN))
    pattern.append(Paragraph(f"Work these 2 rows a total of {heelFlapRows/2} times, ending after a wrong side (purl) row. Begin heel turn as follows:",styleN))
    pattern.append(Paragraph(f"Row 1: k{heelTurnFirstRow}, k2tog, k1, turn",styleN))
    pattern.append(Paragraph(f"Row 2: sl1, p{heelTurnSts+1}, p2tog, p1, turn",styleN))
    pattern.append(Paragraph(f"Row 3: sl1, k{heelTurnSts+2}, k2tog, k1, turn",styleN))
    pattern.append(Paragraph(f"Continue in this fashion until all stitches have been worked. {finalHeelCount} stitches remaining for heel.",styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Knit across {finalHeelCount} heel stitches. Pick up and knit {gussetPU} stitches on the side of the sock (1 stitch in each slipped stitch from the heel flap), place marker for side, knit across {heelFlap} stitches on holder for top of foot, place marker for second side, pick up and knit {gussetPU} more stitches on other side of sock. Knit across {finalHeelCount/2} stitches from heel, place marker. This will be your new beginning of round. Begin gusset decreases as follows:",styleN))
    pattern.append(Paragraph(f"Round 1: Knit to 3 stitches before side marker. k2tog, k1, sl marker, knit across {heelFlap} top of foot stitches, sl marker, k1, ssk, knit to end of round (2 stitches decreased)",styleN))
    pattern.append(Paragraph("Round 2: Knit to end of round",styleN))
    pattern.append(Paragraph(f"Continue these 2 rounds {gussetDecCount-1} more times. {footCount} stitches remaining for foot.",styleN))
    pattern.append(spacer)
    pattern.append(Paragraph(f"Knit in the round until foot length measures {round(footLength-toeLength)} {units} or until sock is {round(toeLength)} {units} less than desired final length. Begin toe decreases as follows:",styleN))
    pattern.append(Paragraph("Round 1: Knit to 3 sts before side marker, k2tog, k1, sl marker, k1, ssk, knit to 3 sts before 2nd side marker, k2tog, k1, sl marker, k1, ssk, knit to end of round (4 stitches decreased)",styleN))
    pattern.append(Paragraph("Round 2: Knit to end of round",styleN))
    pattern.append(Paragraph(f"Continue these 2 rounds {toeDecCount-1} times more {toeCount} stitches remain. Knit to first side marker, and place all stitches from heel and sides onto one DPN, and sts from top of foot onto a 2nd DPN. Graft together with kitchener stitch.",styleN))

    output2 = io.BytesIO()
    c = Canvas(output2) #create pdf
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(page_width/2, page_height-60, "Basic Sock Pattern") #title
    f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1) #frame for pattern
    f.addFromList(pattern,c) #put pattern in frame
    c.showPage()
    c.save()

    pdf2_out = output2.getvalue()
    output2.close()

    response = make_response(pdf2_out)
    response.headers['Content-Disposition'] = "attachment; filename='Basic_Sock_Pattern.pdf"
    response.mimetype = 'application/pdf'
    return response

@app.route("/pattern", methods =["POST"])
def pattern():
    gAnswer = request.form["gaugeAns"]
    sAnswer = request.form["shapeAns"]
    unitType = request.form["units"]
    if(unitType == "inches"):
        units = "inches"
        units2 = "yards"
        units3 = "inch"
    else:
        units = "centimeters"
        units2 = "meters"
        units3 = "cm"
    if(gAnswer == "yes"):
            spi = float(request.form["spi"])
            rpi = float(request.form["rpi"])
    else:
        yarn = request.form["yarn"]

        if(yarn == "lace"):
            spi = 9
            rpi = 11
        else:
            if(yarn == "fingering"):
                spi = 7
                rpi = 9
            else:
                if(yarn == "sport"):
                    spi = 6
                    rpi = 8.5
                else:
                    if(yarn == "dk"):
                        spi = 5.5
                        rpi = 7
                    else:
                        if(yarn == "worsted"):
                            spi = 5
                            rpi = 6
                        else:
                            if(yarn == "aran"):
                                spi = 4
                                rpi = 5.5
                            else:
                                if(yarn == "bulky"):
                                    spi = 3
                                    rpi = 4.5
                                else:
                                    spi = 0
                                    rpi = 0

    if(unitType == "centimeters" and gAnswer == "yes"): #spi/rpi conversion to inches for purposes of needle sizing
        spi = round(spi / 2.54)
        rpi = round(rpi / 2.54)
    needleSizeSm = 0
    needleSizeLg = 0
    #determine recommended needle size and yarn amount based on gauge
    if(spi >= 8):
        needleSizeSm = 000
        needleSizeLg = 1
        yarnNeededSm = 1500
        yarnNeededLg = 3200
    else:
        if(spi < 8 and spi > 6.5):
            needleSizeSm = 1
            needleSizeLg = 3
            yarnNeededSm = 1200
            yarnNeededLg = 2500
        else:
            if(spi <= 6.5 and spi > 5.75):
                needleSizeSm = 3
                needleSizeLg = 5
                yarnNeededSm = 1100
                yarnNeededLg = 2100
            else:
                if(spi <= 5.75 and spi > 5):
                    needleSizeSm = 5
                    needleSizeLg = 6
                    yarnNeededSm = 1000
                    yarnNeededLg = 1800
                else:
                    if(spi <= 5 and spi > 4.5):
                        needleSizeSm = 7
                        needleSizeLg = 8
                        yarnNeededSm = 900
                        yarnNeededLg = 1500
                    else:
                        if(spi <=4.5 and spi > 3.75):
                            needleSizeSm = 8
                            needleSizeLg = 9
                            yarnNeededSm = 700
                            yarnNeededLg = 1200
                        else:
                            if(spi <= 3.75 and spi >= 3):
                                needleSizeSm = 9
                                needleSizeLg = 11
                                yarnNeededSm = 500
                                yarnNeededLg = 800
                            else:
                                needleSizeSm = 11
                                needleSizeLg = 13
                                yarnNeededSm = 400
                                yarnNeededLg = 800

    if(unitType == "centimeters"): #convert yarn amount to meters if cm selected
        yarnNeededSm = round(yarnNeededSm / 1.094)
        yarnNeededLg = round(yarnNeededLg / 1.094)

    if(unitType == "centimeters"): #spi/rpi conversion to cm
        spi = round(spi * 2.54)
        rpi = round(rpi * 2.54)


    neck = float(request.form["neck"])
    bust = float(request.form["bust"])
    waist = float(request.form["waist"])
    hips = float(request.form["hips"])
    arm = float(request.form["arm"])
    wrist = float(request.form["wrist"])
    upperBack = float(request.form["upperBack"])
    upperTorso = float(request.form["upperTorso"])
    lowerTorso = float(request.form["lowerTorso"])
    armLength = float(request.form["armLength"])

    #stitch count calculations
    castOn = round((neck+2)*spi)
    while(castOn%4 !=0):
        castOn += 1

    bustCount = bust * spi
    topSleeveCount = arm * spi
    sleeveCO = round(.06 * waist) * spi
    if(sleeveCO % 2 != 0):
        sleeveCO += 1
    bottomYokeCount = ((topSleeveCount - sleeveCO)*2) + (bustCount-(sleeveCO*2))
    waistCount = (waist + 1) * spi
    bottomCount = hips * spi
    bottomSleeveCount = wrist * spi
    fbNeckCount = round((.8 * castOn)/2)
    if(fbNeckCount % 2 != 0):
        fbNeckCount += 1
    sleeveNeckCount = (castOn - (fbNeckCount * 2))/2
    yokeIncRows = round((bottomYokeCount - castOn)/8)
    if(yokeIncRows % 2 !=0):
        yokeIncRows -= 1
    fbYokeEndCount = fbNeckCount + (yokeIncRows * 2)
    sleeveYokeEndCount = sleeveNeckCount + (yokeIncRows *2)
    bottomYokeCount = (fbYokeEndCount * 2) + (sleeveYokeEndCount * 2)
    bustCount = (fbYokeEndCount * 2) + (sleeveCO * 2)
    topSleeveCount = sleeveYokeEndCount + sleeveCO
    waistDecRows = 0
    hipIncRows = 0
    waistDecs = 0
    hipIncs = 0
    tAnswer = request.form["shapeType"]
    if(sAnswer=="yes"): #shaping variations
        if(tAnswer=="hourglass"):
            waistDecRows = math.floor((bustCount - waistCount)/4)
            if(waistDecRows % 2 != 0): #how many waist decrease rows
               waistDecRows -= 1
            waistCount = bustCount - (waistDecRows * 4) #new waist count
            waistDecs = round((rpi * upperTorso) / waistDecRows) #number of rows for each dec
            hipIncRows = round((bottomCount - waistCount)/4)
            if(hipIncRows % 2 != 0): #how many hip increase rows
                hipIncRows -= 1
            bottomCount = waistCount + (hipIncRows * 4) #new bottom count
            hipIncs = round((rpi * lowerTorso) / hipIncRows) #number of rows for each inc
        else:
            if(tAnswer=="triangle"):
                if(bottomCount > bustCount):
                    hipIncRows = round((bottomCount-bustCount)/4)
                    if(hipIncRows % 2 != 0):
                        hipIncRows -= 1
                    bottomCount = bustCount + (hipIncRows * 4)
                    waistCount = bustCount + ((hipIncRows * 4)/2)
                    hipIncs = round((rpi * (lowerTorso + upperTorso)) / hipIncRows)
                else:
                    if(bottomCount < bustCount):
                        hipIncRows = round((bustCount-bottomCount)/4)
                        if(hipIncRows % 2 != 0):
                            hipIncRows -= 1
                        bottomCount = bustCount - (hipIncRows * 4)
                        waistCount = bustCount - ((hipIncRows * 4)/2)
                        waistDecs = round((rpi * (lowerTorso + upperTorso)) / hipIncRows)
                    else:
                        bottomCount = bustCount
                        waistCount = bustCount
    else: #no waist shaping (straight sweater)
        waistCount = bustCount
        bottomCount = bustCount
    sleeveDecRows = math.floor((topSleeveCount - bottomSleeveCount)/2)
    if(sleeveDecRows % 2 != 0):
        sleeveDecRows -= 1
    bottomSleeveCount = topSleeveCount - (sleeveDecRows * 2)
    sleeveDecs = round((rpi * armLength) / sleeveDecRows)

    #create session variables for pdf
    session['rpi'] = rpi
    session['spi'] = spi
    session['castOn'] = castOn
    session['bustCount'] = bustCount
    session['fbNeckCount'] = fbNeckCount
    session['sleeveNeckCount'] = sleeveNeckCount
    session['yokeIncRows'] = yokeIncRows
    session['bottomYokeCount'] = bottomYokeCount
    session['upperBack'] = upperBack
    session['lowerTorso'] = lowerTorso
    session['upperTorso'] = upperTorso
    session['units'] = units
    session['sleeveYokeEndCount'] = sleeveYokeEndCount
    session['fbYokeEndCount'] = fbYokeEndCount
    session['sleeveCO'] = sleeveCO
    session['waistDecs'] = waistDecs
    session['waistDecRows'] = waistDecRows
    session['waistCount'] = waistCount
    session['hipIncs'] = hipIncs
    session['hipIncRows'] = hipIncRows
    session['bottomCount'] = bottomCount
    session['topSleeveCount'] = topSleeveCount
    session['sleeveDecs'] = sleeveDecs
    session['sleeveDecRows'] = sleeveDecRows
    session['bottomSleeveCount'] = bottomSleeveCount
    session['sAnswer'] = sAnswer
    session['tAnswer'] = tAnswer

    return render_template("pattern.html", spi=spi, rpi=rpi,
    neck=neck, bust=bust, waist=waist, hips=hips, arm=arm, upperBack=upperBack,
    upperTorso=upperTorso, lowerTorso=lowerTorso, armLength=armLength,
    yarnNeededSm=yarnNeededSm, yarnNeededLg=yarnNeededLg, units=units,
    needleSizeSm=needleSizeSm, needleSizeLg=needleSizeLg, units2=units2,
    units3=units3)

@app.route("/sockpattern", methods =["POST"])
def sockpattern():

    gAnswer = request.form["gaugeAns1"]
    mAnswer = request.form["measureTyp"]
    ssAnswer = request.form["gender"]
    unitType = request.form["units1"]
    if(unitType == "inches"):
        units = "inches"
        units3 = "inch"
    else:
        units = "centimeters"
        units3 = "cm"
    if(gAnswer == "yes"):
            spi = float(request.form["spi1"])
            rpi = float(request.form["rpi1"])
    else:
        yarn = request.form["yarn1"]

        if(yarn == "lace"):
            spi = 9
            rpi = 11
        else:
            if(yarn == "fingering"):
                spi = 7
                rpi = 9
            else:
                if(yarn == "sport"):
                    spi = 6
                    rpi = 8.5
                else:
                    if(yarn == "dk"):
                        spi = 5.5
                        rpi = 7
                    else:
                        if(yarn == "worsted"):
                            spi = 5
                            rpi = 6
                        else:
                            if(yarn == "aran"):
                                spi = 4
                                rpi = 5.5
                            else:
                                if(yarn == "bulky"):
                                    spi = 3
                                    rpi = 4.5
                                else:
                                    spi = 0
                                    rpi = 0

    if(unitType == "centimeters" and gAnswer == "yes"): #spi/rpi conversion to inches for purposes of needle sizing
        spi = round(spi / 2.54)
        rpi = round(rpi / 2.54)
    needleSizeSm = 0
    needleSizeLg = 0
    if(spi >= 8):
        needleSizeSm = 000
        needleSizeLg = 1
        yarnNeeded = "between 100 and 150 grams"
    else:
        if(spi < 8 and spi > 6.5):
            needleSizeSm = 1
            needleSizeLg = 3
            yarnNeeded = "between 100 and 150 grams"
        else:
            if(spi <= 6.5 and spi > 5.75):
                needleSizeSm = 3
                needleSizeLg = 5
                yarnNeeded = "between 100 and 150 grams"
            else:
                if(spi <= 5.75 and spi > 5):
                    needleSizeSm = 5
                    needleSizeLg = 6
                    yarnNeeded = "between 100 and 200 grams"
                else:
                    if(spi <= 5 and spi > 4.5):
                        needleSizeSm = 7
                        needleSizeLg = 8
                        yarnNeeded = "between 150 and 200 grams"
                    else:
                        if(spi <=4.5 and spi > 3.75):
                            needleSizeSm = 8
                            needleSizeLg = 9
                            yarnNeeded = "It is not recommended to knit socks from this pattern with yarn this thick"
                        else:
                            if(spi <= 3.75 and spi >= 3):
                                needleSizeSm = 9
                                needleSizeLg = 11
                                yarnNeeded = "It is not recommended to knit socks from this pattern with yarn this thick"
                            else:
                                needleSizeSm = 11
                                needleSizeLg = 13
                                yarnNeeded = "It is not recommended to knit socks from this pattern with yarn this thick"

    if(mAnswer == "footMeas"):
        ankle = float(request.form["ankle"])
        footLength = float(request.form["footLength"])
    else:
        if(ssAnswer == "men"):
            shoeSize = float(request.form["msize"])
            if(shoeSize == 6):
                ankle = 8.25
                footLength = 9.3
            else:
                if(shoeSize == 7):
                    ankle = 8.5
                    footLength = 9.6
                else:
                    if(shoeSize == 8):
                        ankle = 8.75
                        footLength = 10
                    else:
                        if(shoeSize == 9):
                            ankle = 9.25
                            footLength = 10.3
                        else:
                            if(shoeSize == 10):
                                ankle = 9.5
                                footLength = 10.6
                            else:
                                if(shoeSize == 11):
                                    ankle = 9.75
                                    footLength = 11
                                else:
                                    if(shoeSize == 12):
                                        ankle = 10
                                        footLength = 11.3
                                    else:
                                        if(shoeSize == 13):
                                            ankle = 10.25
                                            footLength = 11.6
                                        else:
                                            if(shoeSize == 14):
                                                ankle = 10.5
                                                footLength = 12
                                            else:
                                                ankle = 0
                                                footLength = 0
        else:
            shoeSize = float(request.form["wsize"])
            if(shoeSize == 5):
                ankle = 7.75
                footLength = 8.5
            else:
                if(shoeSize == 6):
                    ankle = 8
                    footLength = 8.9
                else:
                    if(shoeSize == 7):
                        ankle = 8.5
                        footLength = 9.3
                    else:
                        if(shoeSize == 8):
                            ankle = 8.75
                            footLength = 9.5
                        else:
                            if(shoeSize == 9):
                                ankle = 9
                                footLength = 9.9
                            else:
                                if(shoeSize == 10):
                                    ankle = 9.25
                                    footLength = 10.2
                                else:
                                    if(shoeSize == 11):
                                        ankle = 9.5
                                        footLength = 10.5
                                    else:
                                        if(shoeSize == 12):
                                            ankle = 9.75
                                            footLength = 10.9
                                        else:
                                            ankle = 0
                                            footLength = 0


    if(unitType == "centimeters"): #spi/rpi conversion to cm
        spi = round(spi * 2.54)
        rpi = round(rpi * 2.54)
    if(mAnswer=="shoeSize" and unitType=="centimeters"):
        ankle = ankle * 2.54
        footLength = footLength * 2.54

    castOn = round(ankle*spi)
    while(castOn%4 !=0):
        castOn += 1
    heelFlap = castOn/2
    heelFlapRows = heelFlap
    heelTurnSts = round(castOn * .10)
    if(heelTurnSts%2 !=0):
        heelTurnSts -= 1
    heelTurnFirstRow = (heelFlap + heelTurnSts)/2
    finalHeelCount = heelTurnSts + ((heelFlap-heelTurnSts)/2) + 1
    gussetPU = heelFlapRows/2
    gussetCount = finalHeelCount + (gussetPU * 2) + heelFlap
    footCount = castOn
    gussetDecCount = (gussetCount-footCount)/2
    toeCount = 20
    toeDecCount = (castOn-toeCount)/4
    toeLength = 2
    cuffLength = 7
    if(units == "centimeters"):
        toeLength = toeLength * 2.54
        cuffLength = cuffLength * 2.54

    #create session variables for pdf
    session['rpi'] = rpi
    session['spi'] = spi
    session['castOn'] = castOn
    session['heelFlapRows'] = heelFlapRows
    session['heelTurnFirstRow'] = heelTurnFirstRow
    session['heelTurnSts'] = heelTurnSts
    session['finalHeelCount'] = finalHeelCount
    session['gussetPU'] = gussetPU
    session['gussetDecCount'] = gussetDecCount
    session['footCount'] = footCount
    session['footLength'] = footLength
    session['units'] = units
    session['toeLength'] = toeLength
    session['toeDecCount'] = toeDecCount
    session['toeCount'] = toeCount
    session['cuffLength'] = cuffLength
    session['heelFlap'] = heelFlap

    return render_template("sockpattern.html", needleSizeSm=needleSizeSm,
                           needleSizeLg=needleSizeLg, footLength=footLength,
                           ankle=ankle, units3=units3, yarnNeeded=yarnNeeded,
                           rpi=rpi, spi=spi)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(debug=True)
