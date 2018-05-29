#!/usr/bin/env python

import sys,os
from math import sqrt
import ROOT as rt
import CMS_lumi, tdrstyle

from efficiencyUtils import efficiency
from efficiencyUtils import efficiencyList
import efficiencyUtils as effUtil

tdrstyle.setTDRStyle()


effiMin = 0.68
effiMax = 1.07

sfMin = 0.78
sfMax = 1.12


def isFloat( myFloat ):
    try:
        float(myFloat)
        return True
    except:
        return False



graphColors = [rt.kBlack, rt.kRed, rt.kBlue, rt.kRed-2, rt.kAzure+2, rt.kAzure-1, 
               rt.kSpring-1, rt.kYellow -2 , rt.kYellow+1,
               rt.kBlack, rt.kBlack, rt.kBlack, 
               rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack ]




def findMinMax( effis ):
    mini = +999
    maxi = -999

    for key in effis.keys():
        for eff in effis[key]:
            if eff['val'] - eff['errlow'] < mini:
                mini = eff['val'] - eff['errlow']
            if eff['val'] + eff['errhigh'] > maxi:
                maxi = eff['val'] + eff['errhigh']

    if mini > 0.18 and mini < 0.28:
        mini = 0.18
    if mini > 0.28 and mini < 0.38:
        mini = 0.28
    if mini > 0.38 and mini < 0.48:
        mini = 0.38
    if mini > 0.48 and mini < 0.58:
        mini = 0.48
    if mini > 0.58 and mini < 0.68:
        mini = 0.58
    if mini > 0.68 and mini < 0.78:
        mini = 0.68
    if mini > 0.78 and mini < 0.88:
        mini = 0.78
    if mini > 0.88:
        mini = 0.88
    if mini > 0.92:
        mini = 0.92

        
    if  maxi > 0.95:
        maxi = 1.17        
    elif maxi < 0.87:
        maxi = 0.87
    else:
        maxi = 1.07

    if maxi-mini > 0.5:
        maxi = maxi + 0.2
        
    return (mini,maxi)

#### added by me: draw data/mc plot with multiple data 
def EffiGraph1D_multiData(effDataLists, effMCList, sfLists ,nameout, fileNameList, xAxis = 'pT', yAxis = 'eta', EB_or_EE = 'EB'):

            
    W = 800
    H = 800
    yUp = 0.3
    canName = 'toto' + xAxis + EB_or_EE

    c = rt.TCanvas(canName,canName,50,50,H,W)
    c.SetTopMargin(0.055)
    c.SetBottomMargin(0.10)
    c.SetLeftMargin(0.12)
    
    
    p1 = rt.TPad( canName + '_up', canName + '_up', 0, yUp + 0.001, 1,   1, 0,0,0)
    p2 = rt.TPad( canName + '_do', canName + '_do', 0,   0, 1, yUp, 0,0,0)
    p1.SetBottomMargin(0.02)
    p1.SetTopMargin(   c.GetTopMargin()*1/(1-yUp))
    p1.SetGridy()
    p2.SetTopMargin(   0.0075)
    p2.SetBottomMargin( c.GetBottomMargin()*1/yUp)
    p1.SetLeftMargin( c.GetLeftMargin() )
    p2.SetLeftMargin( c.GetLeftMargin() )
    firstGraph = True
    #leg = rt.TLegend(0.35, 0.8, 0.65 ,0.93) # for eta, nvtx
    leg = rt.TLegend(0.35, 0.8, 0.65 ,0.93) # for et plot
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    igr = 0
    listOfTGraph1 = []
    listOfTGraph2 = []
    listOfMC      = []

    xMin = 10
    xMax = 200
    if 'pT' in xAxis or 'pt' in xAxis:
        p1.SetLogx()
        p2.SetLogx()    
        xMin = 10
        xMax = 250
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        xMin =  0
        xMax = 70
    elif 'eta' in xAxis or 'Eta' in xAxis:
        xMin = -2.50
        xMax = +2.50
    elif 'phi' in xAxis or 'Phi' in xAxis:
        xMin = -3.15
        xMax = +3.15
    elif 'z' in xAxis or 'Z' in xAxis:
        xMin = 0
        xMax = 20
    
    if 'abs' in xAxis or 'Abs' in xAxis:
        xMin = 0.0

    # loop over effGraphList and save them into listOfTGraph
    idx_sfList = 0
    for list_ in effDataLists :
   
        if 'eta' not in xAxis :
           if 'EB' == EB_or_EE :
              #effDataList = list_.pt_1DGraph_list_EB( False )
              effDataList = list_.pt_1DGraph_list_AsymError_EB( False , False)
              #effMCList = list_.pt_1DGraph_list_EB_MC()
              effMCList = list_.pt_1DGraph_list_AsymError_EB(False, True)
              #sfList = sfLists[idx_sfList].pt_1DGraph_list_EB( True )
              sfList = sfLists[idx_sfList].pt_1DGraph_list_AsymError_EB( True, False )
              name = fileNameList[idx_sfList]
           elif 'EE' == EB_or_EE :
              #effDataList = list_.pt_1DGraph_list_EE( False )
              effDataList = list_.pt_1DGraph_list_AsymError_EE( False, False)
              #effMCList = list_.pt_1DGraph_list_EE_MC()
              effMCList = list_.pt_1DGraph_list_AsymError_EE(False, True)
              #sfList = sfLists[idx_sfList].pt_1DGraph_list_EE( True )
              sfList = sfLists[idx_sfList].pt_1DGraph_list_AsymError_EE( True, False )
              name = fileNameList[idx_sfList]
        elif 'eta' in xAxis :
              effDataList = list_.eta_1DGraph_list( False )
              effMCList = list_.eta_1DGraph_list_MC()
              sfList = sfLists[idx_sfList].eta_1DGraph_list( True )              
              name = fileNameList[idx_sfList]

    
        effminmax =  findMinMax( effDataList )
        effiMin = effminmax[0]
        effiMax = effminmax[1]
    
        sfminmax =  findMinMax( sfList )
        sfMin = sfminmax[0]
    
        for key in sorted(effDataList.keys()):
            grBinsEffData = effUtil.makeTGraphFromList_v3(effDataList[key], 'min', 'max')
            grBinsSF      = effUtil.makeTGraphFromList(sfList[key]     , 'min', 'max')
            grBinsEffMC = None
            if not effMCList is None:
                grBinsEffMC = effUtil.makeTGraphFromList_v3(effMCList[key], 'min', 'max')
                grBinsEffMC.SetLineColor( rt.kBlack )
                grBinsEffMC.SetMarkerStyle( 24 )
                grBinsEffMC.SetLineWidth( 1 )
    
            grBinsSF     .SetMarkerColor( graphColors[igr] )
            grBinsSF     .SetLineColor(   graphColors[igr] )
            grBinsSF     .SetLineWidth(2)
            grBinsEffData.SetMarkerColor( graphColors[igr] )
            grBinsEffData.SetLineColor(   graphColors[igr] )
            grBinsEffData.SetLineWidth(2) 
                    
            grBinsEffData.GetHistogram().SetMinimum(effiMin)
            grBinsEffData.GetHistogram().SetMaximum(effiMax)
    
            grBinsEffData.GetHistogram().GetXaxis().SetLimits(xMin,xMax)
            grBinsSF.GetHistogram()     .GetXaxis().SetLimits(xMin,xMax)
            grBinsSF.GetHistogram().SetMinimum(sfMin)
            grBinsSF.GetHistogram().SetMaximum(sfMax)
            
            grBinsSF.GetHistogram().GetXaxis().SetTitleOffset(1)
            if 'eta' in xAxis or 'Eta' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("SC #eta")
            elif 'pt' in xAxis or 'pT' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("SC E_{T}  [GeV]")  
            elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("N_{vtx}")  
            elif 'phi' in xAxis or 'Phi' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("SC #phi")
            elif 'z' in xAxis or 'Z' in xAxis :
                grBinsSF.GetHistogram().GetXaxis().SetTitle("z [cm]")
                
            grBinsSF.GetHistogram().GetYaxis().SetTitle("Data / MC " )
            grBinsSF.GetHistogram().GetYaxis().SetTitleOffset(1)
                
            grBinsEffData.GetHistogram().GetYaxis().SetTitleOffset(1)
            grBinsEffData.GetHistogram().GetYaxis().SetTitle("Efficiency" )
            grBinsEffData.GetHistogram().GetYaxis().SetRangeUser( effiMin, effiMax )
    
            ### to avoid loosing the TGraph keep it in memory by adding it to a list
            listOfTGraph1.append( grBinsEffData )
            listOfTGraph2.append( grBinsSF ) 
            listOfMC.append( grBinsEffMC   )

            if 'eta' in yAxis or 'Eta' in yAxis:
                #leg.AddEntry( grBinsEffData, '%1.3f #leq | #eta | #leq  %1.3f' % (float(key[0]),float(key[1])), "PL")        
                leg.AddEntry( grBinsEffData,  name, "PL")        
                #leg.AddEntry( grBinsEffData, "2017 (35.8 /fb)", "PL")        
            elif 'pt' in yAxis or 'pT' in yAxis:
                #leg.AddEntry( grBinsEffData, '%3.0f #leq p_{T} #leq  %3.0f GeV' % (float(key[0]),float(key[1])), "PL")        
                leg.AddEntry( grBinsEffData, name, "PL")        
                #leg.AddEntry( grBinsEffData, "2017 (35.8 /fb)", "PL")        
            elif 'vtx' in yAxis or 'Vtx' in yAxis or 'PV' in yAxis:
                leg.AddEntry( grBinsEffData, '%3.0f #leq nVtx #leq  %3.0f'      % (float(key[0]),float(key[1])), "PL")        

      
        idx_sfList = idx_sfList + 1

    if not effMCList is None:
       leg.AddEntry( grBinsEffMC, 'MC', "PL")

    for igr in range(len(listOfTGraph1)+1):

        option = "PE"
        if igr == 1:
            option = "APE"

        use_igr = igr
        if use_igr == len(listOfTGraph1):
            use_igr = 0
            
        listOfTGraph1[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph1[use_igr].SetMarkerColor(graphColors[use_igr])
        #if not listOfMC[use_igr] is None:
        #    listOfMC[use_igr].SetLineColor(graphColors[use_igr])

        listOfTGraph1[use_igr].GetHistogram().SetMinimum(effiMin)
        listOfTGraph1[use_igr].GetHistogram().SetMinimum(0.92)
        listOfTGraph1[use_igr].GetHistogram().SetMaximum(1.05)

        #listOfTGraph1[use_igr].GetHistogram().SetMaximum(1.05) # et plot

        listOfTGraph1[use_igr].GetHistogram().SetLabelSize(0)

        p1.cd()
        listOfTGraph1[use_igr].Draw(option)
        if not listOfMC[use_igr] is None:
            #listOfMC[use_igr].Draw("ez")
            listOfMC[use_igr].Draw("pesame")

        p2.cd()            
        listOfTGraph2[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph2[use_igr].SetMarkerColor(graphColors[use_igr])
        listOfTGraph2[use_igr].GetHistogram().SetMinimum(sfMin)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(sfMax)

        listOfTGraph2[use_igr].GetHistogram().SetMinimum(0.87)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(1.12)

        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetLabelSize(0.1)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleSize(0.09)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleOffset(0.7)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetLabelSize(0.1)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleSize(0.09)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleOffset(1.2)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetNdivisions(505)

        if 'pT' in xAxis or 'pt' in xAxis :
            listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetMoreLogLabels()
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetNoExponent()
        listOfTGraph2[use_igr].Draw(option)

    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)
    
    p2.cd()
    lineAtOne.Draw()

    c.cd()
    p2.Draw()
    p1.Draw()

    leg.Draw()

    eb_ee = rt.TLatex()
    if 'eta' not in xAxis :
        eb_ee.SetTextSize(0.03)
        if 'EB' == EB_or_EE : eb_ee.DrawLatex(0.65,0.9, "|#eta_{SC}| < 1.479") # for et plot
        if 'EE' == EB_or_EE : eb_ee.DrawLatex(0.65,0.9, "|#eta_{SC}| > 1.479")

        #if 'EB' == EB_or_EE : eb_ee.DrawLatex(0.52,0.9, "|#eta_{SC}| < 1.479")
        #if 'EE' == EB_or_EE : eb_ee.DrawLatex(0.52,0.9, "|#eta_{SC}| > 1.479")

    CMS_lumi.CMS_lumi(c, 4, 10)

    c.Print(nameout)
####   

def EffiGraph1D(effDataList, effMCList, sfList ,nameout, xAxis = 'pT', yAxis = 'eta', EB_or_EE = 'EB'):
            
    W = 800
    H = 800
    yUp = 0.3
    canName = 'toto' + xAxis + EB_or_EE

    c = rt.TCanvas(canName,canName,50,50,H,W)
    c.SetTopMargin(0.055)
    c.SetBottomMargin(0.10)
    c.SetLeftMargin(0.12)
    
    
    p1 = rt.TPad( canName + '_up', canName + '_up', 0, yUp, 1,   1, 0,0,0)
    p2 = rt.TPad( canName + '_do', canName + '_do', 0,   0, 1, yUp, 0,0,0)
    p1.SetBottomMargin(0.0075)
    p1.SetTopMargin(   c.GetTopMargin()*1/(1-yUp))
    p1.SetGridy()
    p2.SetTopMargin(   0.0075)
    p2.SetBottomMargin( c.GetBottomMargin()*1/yUp)
    p1.SetLeftMargin( c.GetLeftMargin() )
    p2.SetLeftMargin( c.GetLeftMargin() )
    firstGraph = True
    leg = rt.TLegend(0.5,0.80,0.95 ,0.92)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    igr = 0
    listOfTGraph1 = []
    listOfTGraph2 = []
    listOfMC      = []

    xMin = 10
    xMax = 200
    if 'pT' in xAxis or 'pt' in xAxis:
        #p1.SetLogx()
        #p2.SetLogx()    
        xMin = 10
        xMax = 100
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        xMin =  0
        xMax = 60
    elif 'eta' in xAxis or 'Eta' in xAxis:
        xMin = -2.50
        xMax = +2.50
    elif 'phi' in xAxis or 'Phi' in xAxis:
        xMin = -3.15
        xMax = +3.15
    elif 'z' in xAxis or 'Z' in xAxis:
        xMin = 0
        xMax = 20
    
    if 'abs' in xAxis or 'Abs' in xAxis:
        xMin = 0.0

    effminmax =  findMinMax( effDataList )
    effiMin = effminmax[0]
    effiMax = effminmax[1]

    sfminmax =  findMinMax( sfList )
    sfMin = sfminmax[0]
#    sfMin = 0.94
#    sfMax = 1.02

    for key in sorted(effDataList.keys()):
        grBinsEffData = effUtil.makeTGraphFromList(effDataList[key], 'min', 'max')
        grBinsSF      = effUtil.makeTGraphFromList(sfList[key]     , 'min', 'max')
        grBinsEffMC = None
        if not effMCList is None:
            grBinsEffMC = effUtil.makeTGraphFromList(effMCList[key], 'min', 'max')
            grBinsEffMC.SetLineStyle( rt.kDashed )
            grBinsEffMC.SetLineColor( graphColors[igr] )
            grBinsEffMC.SetMarkerSize( 0 )
            grBinsEffMC.SetLineWidth( 2 )

        grBinsSF     .SetMarkerColor( graphColors[igr] )
        grBinsSF     .SetLineColor(   graphColors[igr] )
        grBinsSF     .SetLineWidth(2)
        grBinsEffData.SetMarkerColor( graphColors[igr] )
        grBinsEffData.SetLineColor(   graphColors[igr] )
        grBinsEffData.SetLineWidth(2) 
                
        grBinsEffData.GetHistogram().SetMinimum(effiMin)
        grBinsEffData.GetHistogram().SetMaximum(effiMax)

        grBinsEffData.GetHistogram().GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram()     .GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram().SetMinimum(sfMin)
        grBinsSF.GetHistogram().SetMaximum(sfMax)
        
        grBinsSF.GetHistogram().GetXaxis().SetTitleOffset(1)
        if 'eta' in xAxis or 'Eta' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("SC #eta")
        elif 'pt' in xAxis or 'pT' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("SC E_{T}  [GeV]")  
        elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("N_{vtx}")  
        elif 'phi' in xAxis or 'Phi' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("SC #phi")
        elif 'z' in xAxis or 'Z' in xAxis :
            grBinsSF.GetHistogram().GetXaxis().SetTitle("z [cm]")
            
        grBinsSF.GetHistogram().GetYaxis().SetTitle("Data / MC " )
        grBinsSF.GetHistogram().GetYaxis().SetTitleOffset(1)
            
        grBinsEffData.GetHistogram().GetYaxis().SetTitleOffset(1)
        grBinsEffData.GetHistogram().GetYaxis().SetTitle("Data efficiency" )
        grBinsEffData.GetHistogram().GetYaxis().SetRangeUser( effiMin, effiMax )

            
        ### to avoid loosing the TGraph keep it in memory by adding it to a list
        listOfTGraph1.append( grBinsEffData )
        listOfTGraph2.append( grBinsSF ) 
        listOfMC.append( grBinsEffMC   )
        if 'eta' in yAxis or 'Eta' in yAxis:
            leg.AddEntry( grBinsEffData, '%1.3f #leq | #eta | #leq  %1.3f' % (float(key[0]),float(key[1])), "PL")        
        elif 'pt' in yAxis or 'pT' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq p_{T} #leq  %3.0f GeV' % (float(key[0]),float(key[1])), "PL")        
        elif 'vtx' in yAxis or 'Vtx' in yAxis or 'PV' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq nVtx #leq  %3.0f'      % (float(key[0]),float(key[1])), "PL")        

        
    for igr in range(len(listOfTGraph1)+1):

        option = "P"
        if igr == 1:
            option = "AP"

        use_igr = igr
        if use_igr == len(listOfTGraph1):
            use_igr = 0
            
        listOfTGraph1[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph1[use_igr].SetMarkerColor(graphColors[use_igr])
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].SetLineColor(graphColors[use_igr])

        #listOfTGraph1[use_igr].GetHistogram().SetMinimum(effiMin)
        listOfTGraph1[use_igr].GetHistogram().SetMinimum(0.01)
        listOfTGraph1[use_igr].GetHistogram().SetMaximum(1.3)
        p1.cd()
        print "igr: " + str(igr) + " option: " + option
        if igr == 2 : continue
        listOfTGraph1[use_igr].Draw(option)
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].Draw("ez")

        p2.cd()            
        listOfTGraph2[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph2[use_igr].SetMarkerColor(graphColors[use_igr])
        listOfTGraph2[use_igr].GetHistogram().SetMinimum(sfMin)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(sfMax)

        listOfTGraph2[use_igr].GetHistogram().SetMinimum(0.87)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(1.12)

        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetLabelSize(0.09)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleSize(0.09)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleOffset(0.7)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetLabelSize(0.09)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleSize(0.09)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleOffset(1.2)
        if 'pT' in xAxis or 'pt' in xAxis :
            listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetMoreLogLabels()
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetNoExponent()
        listOfTGraph2[use_igr].Draw(option)
        

    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)
    
    p2.cd()
    lineAtOne.Draw()

    c.cd()
    p2.Draw()
    p1.Draw()

    if 'pT' in xAxis or 'pt' in xAxis:
        leg.Draw()
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        leg.Draw()
    elif 'phi' in xAxis or 'Phi' in xAxis:
        leg.Draw()
    elif 'z' in xAxis or 'Z' in xAxis:
        leg.Draw()

    CMS_lumi.CMS_lumi(c, 4, 10)

    c.Print(nameout)

    #################################################    


def diagnosticErrorPlot( effgr, ierror, nameout ):
    errorNames = efficiency.getSystematicNames()
    c2D_Err = rt.TCanvas('canScaleFactor_%s' % errorNames[ierror] ,'canScaleFactor: %s' % errorNames[ierror],1000,600)    
    c2D_Err.Divide(2,1)
    c2D_Err.GetPad(1).SetLogy()
    c2D_Err.GetPad(2).SetLogy()
    c2D_Err.GetPad(1).SetRightMargin(0.15)
    c2D_Err.GetPad(1).SetLeftMargin( 0.15)
    c2D_Err.GetPad(1).SetTopMargin(  0.10)
    c2D_Err.GetPad(2).SetRightMargin(0.15)
    c2D_Err.GetPad(2).SetLeftMargin( 0.15)
    c2D_Err.GetPad(2).SetTopMargin(  0.10)

    h2_sfErrorAbs = effgr.ptEtaScaleFactor_2DHisto(ierror+1, False )
    h2_sfErrorRel = effgr.ptEtaScaleFactor_2DHisto(ierror+1, True  )
    h2_sfErrorAbs.SetMinimum(0)
    h2_sfErrorAbs.SetMaximum(min(h2_sfErrorAbs.GetMaximum(),0.2))
    h2_sfErrorRel.SetMinimum(0)
    h2_sfErrorRel.SetMaximum(1)
    h2_sfErrorAbs.SetTitle('e/#gamma absolute SF syst: %s ' % errorNames[ierror])
    h2_sfErrorRel.SetTitle('e/#gamma relative SF syst: %s ' % errorNames[ierror])
    c2D_Err.cd(1)
    h2_sfErrorAbs.DrawCopy("colz TEXT45")
    c2D_Err.cd(2)
    h2_sfErrorRel.DrawCopy("colz TEXT45")
    
    c2D_Err.Print(nameout)

#### added by me: draw 1D plot with multiple data

def draw1Dplots(filesin, lumi, outdir, axis = ['pT','eta']):

    effGraphList = []
    dataNameList = []
    print filesin
    
    for filein in filesin :
        fileWithEff = open(filein, 'r')
        print 'open ' + filein
     
    
        temp_effGraph = efficiencyList()    
        #temp_name = filein.replace('/','_').split('_')[7] + '_' + filein.replace('/','_').split('_')[9]
        temp_name =  filein.replace('/','_').split('_')[9]
        print  temp_name
    
        for line in fileWithEff :
            modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
            numbers = modifiedLine.split('\t')
    
            if len(numbers) > 0 and isFloat(numbers[0]):
                etaKey = ( float(numbers[0]), float(numbers[1]) )
                ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )
    
                myeff = efficiency(ptKey,etaKey,
                                   float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),
                                   float(numbers[8]),float(numbers[9]),float(numbers[10]),float(numbers[11]) )
    
    
    
                temp_effGraph.addEfficiency(myeff)
    
    
        fileWithEff.close()
    
        temp_effGraph.symmetrizeSystVsEta()
        temp_effGraph.combineSyst()
        
        dataNameList.append(temp_name) 
        effGraphList.append(temp_effGraph) #### 
    
    pdfout = outdir + '/egammaPlots.pdf'

    if 'eta' in axis[0] :
        EffiGraph1D_multiData( effGraphList , #eff Data
                      None,
                      effGraphList , #SF
                      pdfout,
                      dataNameList,    
                      xAxis = axis[0], yAxis = axis[1] )
    else :

         EffiGraph1D_multiData( effGraphList , #eff Data
                      None,
                      effGraphList , #SF
                      pdfout,
                      dataNameList,
                      xAxis = axis[0], yAxis = axis[1] )

         EffiGraph1D_multiData( effGraphList , #eff Data
                      None,
                      effGraphList , #SF
                      pdfout + '_EE.pdf',
                      dataNameList,
                      xAxis = axis[0], yAxis = axis[1] , EB_or_EE = 'EE')
####

#### added by me: draw 1D plot with data/mc 
def draw1Dplot(filein, lumi, outdir, axis = ['pT','eta']):
    print " Opening file: %s (plot lumi: %3.1f)" % ( filein, lumi )
    CMS_lumi.lumi_13TeV = "%+3.1f fb^{-1}" % lumi

    nameOutBase = filein
    if not os.path.exists( filein ) :
        print 'file %s does not exist' % filein
        sys.exit(1)

    fileWithEff = open(filein, 'r')
    effGraph = efficiencyList()  ### Lets try to make list of effGraph!

    ####
    effGraphList = []
    ####

    for line in fileWithEff :
        modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
        numbers = modifiedLine.split('\t')

        if len(numbers) > 0 and isFloat(numbers[0]):
            etaKey = ( float(numbers[0]), float(numbers[1]) )
            ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )

            myeff = efficiency(ptKey,etaKey,
                               float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),
                               float(numbers[8]),float(numbers[9]),float(numbers[10]),float(numbers[11]) )



            effGraph.addEfficiency(myeff)
       

    fileWithEff.close()

    effGraph.symmetrizeSystVsEta()
    effGraph.combineSyst()

    effGraphList.append(effGraph) #### test

    pdfout = outdir + '/egammaPlots.pdf'
    #cDummy = rt.TCanvas()
    #cDummy.Print( pdfout + "[" )

    #EffiGraph1D_noRatioPlot( effGraph.pt_1DGraph_list( False ) , #eff Data
    #                         pdfout,
    #                         xAxis = axis[0], yAxis = axis[1] )
#    EffiGraph1D( effGraph.pt_1DGraph_list_EB( False ) , #eff Data
#                 None,
#                 effGraph.pt_1DGraph_list_EB( True ) , #SF
#                 pdfout,
#                 xAxis = axis[0], yAxis = axis[1] )
#
#    EffiGraph1D( effGraph.pt_1DGraph_list_EE( False ) , #eff Data
#                 None,
#                 effGraph.pt_1DGraph_list_EE( True ) , #SF
#                 pdfout + '_test.pdf',
#                 xAxis = axis[0], yAxis = axis[1] , EB_or_EE = 'EE')
#
    if 'eta' in axis[0]: 
        EffiGraph1D( effGraph.eta_1DGraph_list( False ) , #eff Data # no comaprison between EB and EE
                     None,
                     effGraph.eta_1DGraph_list( True ) , #SF
                     pdfout,
                     xAxis = axis[0], yAxis = axis[1] )

    else: 
        EffiGraph1D( effGraph.pt_1DGraph_list( False ) , #eff Data
                 None,
                 effGraph.pt_1DGraph_list( True ) , #SF
                 pdfout,
                 xAxis = axis[0], yAxis = axis[1] )

        #EffiGraph1D( effGraph.pt_1DGraph_list_EB( False ) , #eff Data
        #             None,
        #             effGraph.pt_1DGraph_list_EB( True ) , #SF
        #             pdfout,
        #             xAxis = axis[0], yAxis = axis[1] )

        #EffiGraph1D( effGraph.pt_1DGraph_list_EE( False ) , #eff Data
        #         None,
        #         effGraph.pt_1DGraph_list_EE( True ) , #SF
        #         pdfout + '_test.pdf',
        #         xAxis = axis[0], yAxis = axis[1] , EB_or_EE = 'EE')

    #cDummy.Print( pdfout + "]" )
####


def doEGM_SFs(filein, lumi, axis = ['pT','eta'] ):
    print " Opening file: %s (plot lumi: %3.1f)" % ( filein, lumi )
    CMS_lumi.lumi_13TeV = "%+3.1f fb^{-1}" % lumi 

    nameOutBase = filein 
    if not os.path.exists( filein ) :
        print 'file %s does not exist' % filein
        sys.exit(1)


    fileWithEff = open(filein, 'r')
    effGraph = efficiencyList()
    
    for line in fileWithEff :
        modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
        numbers = modifiedLine.split('\t')

        if len(numbers) > 0 and isFloat(numbers[0]):
            etaKey = ( float(numbers[0]), float(numbers[1]) )
            ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )
        
            myeff = efficiency(ptKey,etaKey,
                               float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),
                               float(numbers[8]),float(numbers[9]),float(numbers[10]),float(numbers[11]) )
#                           float(numbers[8]),float(numbers[9]),float(numbers[10]), -1 )

            effGraph.addEfficiency(myeff)

    fileWithEff.close()

### massage the numbers a bit
    effGraph.symmetrizeSystVsEta()
    effGraph.combineSyst()

    print " ------------------------------- "

    customEtaBining = []
    customEtaBining.append( (0.000,0.800))
    customEtaBining.append( (0.800,1.444))
    customEtaBining.append( (1.444,1.566))
    customEtaBining.append( (1.566,2.000))
    customEtaBining.append( (2.000,2.500))


    pdfout = nameOutBase + '_egammaPlots.pdf'
    cDummy = rt.TCanvas()
    cDummy.Print( pdfout + "[" )


    EffiGraph1D( effGraph.pt_1DGraph_list( False ) , #eff Data
                 None, 
                 effGraph.pt_1DGraph_list( True ) , #SF
                 pdfout,
                 xAxis = axis[0], yAxis = axis[1] )
#EffiGraph1D( effGraph.pt_1DGraph_list_customEtaBining(customEtaBining,False) , 
#             effGraph.pt_1DGraph_list_customEtaBining(customEtaBining,True)   , False, pdfout )
#    EffiGraph1D( effGraph.eta_1DGraph_list(False), effGraph.eta_1DGraph_list(True), True , pdfout )
    listOfSF1D = EffiGraph1D( effGraph.eta_1DGraph_list( typeGR =  0 ) , # eff Data
                              effGraph.eta_1DGraph_list( typeGR = -1 ) , # eff MC
                              effGraph.eta_1DGraph_list( typeGR = +1 ) , # SF
                              pdfout, 
                              xAxis = axis[1], yAxis = axis[0] )

    h2EffData = effGraph.ptEtaScaleFactor_2DHisto(-3)
    h2EffMC   = effGraph.ptEtaScaleFactor_2DHisto(-2)
    h2SF      = effGraph.ptEtaScaleFactor_2DHisto(-1)
    h2Error   = effGraph.ptEtaScaleFactor_2DHisto( 0)  ## only error bars

    rt.gStyle.SetPalette(1)
    rt.gStyle.SetPaintTextFormat('1.3f');
    rt.gStyle.SetOptTitle(1)

    c2D = rt.TCanvas('canScaleFactor','canScaleFactor',900,600)
    c2D.Divide(2,1)
    c2D.GetPad(1).SetRightMargin(0.15)
    c2D.GetPad(1).SetLeftMargin( 0.15)
    c2D.GetPad(1).SetTopMargin(  0.10)
    c2D.GetPad(2).SetRightMargin(0.15)
    c2D.GetPad(2).SetLeftMargin( 0.15)
    c2D.GetPad(2).SetTopMargin(  0.10)
    c2D.GetPad(1).SetLogy()
    c2D.GetPad(2).SetLogy()
    

    c2D.cd(1)
    dmin = 1.0 - h2SF.GetMinimum()
    dmax = h2SF.GetMaximum() - 1.0
    dall = max(dmin,dmax)
    h2SF.SetMinimum(1-dall)
    h2SF.SetMaximum(1+dall)
    h2SF.DrawCopy("colz TEXT45")
    
    c2D.cd(2)
    h2Error.SetMinimum(0)
    h2Error.SetMaximum(min(h2Error.GetMaximum(),0.2))    
    h2Error.DrawCopy("colz TEXT45")

    c2D.Print( pdfout )


    rootout = rt.TFile(nameOutBase + '_EGM2D.root','recreate')
    rootout.cd()
    h2SF.Write('EGamma_SF2D',rt.TObject.kOverwrite)
    h2EffData.Write('EGamma_EffData2D',rt.TObject.kOverwrite)
    h2EffMC  .Write('EGamma_EffMC2D'  ,rt.TObject.kOverwrite)
    for igr in range(len(listOfSF1D)):
        listOfSF1D[igr].Write( 'grSF1D_%d' % igr, rt.TObject.kOverwrite)
    rootout.Close()

    for isyst in range(len(efficiency.getSystematicNames())):
        diagnosticErrorPlot( effGraph, isyst, pdfout )

    cDummy.Print( pdfout + "]" )



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='tnp EGM scale factors')
    parser.add_argument('--lumi'  , type = float, default = -1, help = 'Lumi (just for plotting purpose)')
    parser.add_argument('txtFile' , default = None, help = 'EGM formatted txt file')
    parser.add_argument('--PV'    , action  = 'store_true', help = 'plot 1 vs nVtx instead of pT' )
    args = parser.parse_args()

    if args.txtFile is None:
        print ' - Needs EGM txt file as input'
        sys.exit(1)
    

    CMS_lumi.lumi_13TeV = "5.5 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.lumi_sqrtS = "13 TeV"
    
    axis = ['pT','eta']
    if args.PV:
        axis = ['nVtx','eta']

    doEGM_SFs(args.txtFile, args.lumi,axis)
