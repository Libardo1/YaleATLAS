import numpy as np
import pandas as pd 

def cutEvents_1btag(df, btag_branch):
    '''
    Args:
    -----
            df: pandas dataframe containing your data
            btag_branch: string with the name of the branch to be used for b-tagging purposes
    Returns:
    --------
            df_1btag: pandas dataframe generated from the input one by selecting only events with 1 b-tagged jet
    Note:
    -----

    '''

    # -- slice df by only considering events with == 1 b-tagged jet:
    df_1btag = df[np.asarray([np.sum(event) for event in df[btag_branch]]) == 1]

    return df_1btag

############################################################

def pair_highestPt(df_1btag, btag_branch, pt_branch):
    '''
    Args:
    -----
            df_1btag: pandas dataframe containing events with only 1 b-tagged jet
            btag_branch: string with the name of the branch to be used for b-tagging purposes
            pt_branch: string with the name of the branch with jets' pt's
    Returns:
    --------
            pair_indices: list of np arrays of sorted indices of the two selected jets
    Note:
    -----

    '''

    pair_indices = []

    for event in df_1btag.index.values:

        if event%10000 == 0:
            print 'Processing event {} of {}'.format(event, df_1btag.shape[0])

        # -- find the second jet among the non b-tagged ones by picking the one with highest pT:
        selected_index = np.argmax((df_1btag[pt_branch].at[event])[(df_1btag[btag_branch].at[event]) == 0])
        # -- get the index of the b-jet that is already b-tagged
        firstjet_index = np.argmax(df_1btag[btag_branch].at[event])
        
        # -- shift the index of the selected jet by 1 if it comes after the one that is already b-tagged
        if firstjet_index <= selected_index:
            selected_index += 1  

        pair_indices.append(np.sort([firstjet_index, selected_index]))

    return pair_indices

############################################################

def pair_HiggsMass(df_1btag, btag_branch, pt_branch, eta_branch, phi_branch, m_branch):
    '''
    Args:
    -----
            df_1btag: pandas dataframe containing events with only 1 b-tagged jet
            btag_branch: string with the name of the branch to be used for b-tagging purposes
            pt_branch: string with the name of the branch with jets' pt's
            eta_branch: string with the name of the branch with jets' etas
            phi_branch: string with the name of the branch with jets' phis
            m_branch: string with the name of the branch with jets' masses
    Returns:
    --------
            pair_indices: list of np arrays of sorted indices of the two selected jets
    Note:
    -----

    '''

    pair_indices = []

    for event in df_1btag.index.values:

        if event%10000 == 0:
            print 'Processing event {} of {}'.format(event, df_1btag.shape[0])
            
        # -- find the second jet among the non b-tagged ones by picking the one that gives the reco mass closest to 125 GeV:
        firstjet_index = np.argmax(df_1btag[btag_branch].at[event])
        
        # -- calculate the 4vector of the b-tagged jet
        p1 = LorentzVector()
        p1.SetPtEtaPhiM( 
            (df_1btag[pt_branch].at[event])[firstjet_index],
            (df_1btag[eta_branch].at[event])[firstjet_index],
            (df_1btag[phi_branch].at[event])[firstjet_index],
            (df_1btag[m_branch].at[event])[firstjet_index]
        )

        # -- total number of jets per event
        njets = (df_1btag[[pt_branch]].at[event]).shape[0]
        
        # -- ugly, find better way?
        diff = 999999999999
        for jet in xrange(njets):
            if jet != firstjet_index: # exclude the already b-tagged jet itself
                p2 = LorentzVector()
                p2.SetPtEtaPhiM( 
                    (df_1btag[pt_branch].at[event])[jet],
                    (df_1btag[eta_branch].at[event])[jet],
                    (df_1btag[phi_branch].at[event])[jet],
                    (df_1btag[m_branch].at[event])[jet]
                )
                recomass = (p1+p2).M() # reconstructed mass of current jet and b-tagged jet

                # -- calculate the discriminating variable
                new_diff = abs(125000 - recomass)

                if new_diff < diff: # if we found the best jet yet
                    diff = new_diff
                    selected_index = jet

        pair_indices.append(np.sort([firstjet_index, selected_index]))

    return pair_indices

