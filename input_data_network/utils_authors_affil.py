# built-in
from itertools import combinations

# third party
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.cm as cm


def get_bigrams(filepath):

    print('\nGetting all possible combinations of authors and counting their shared papers...')

    df = pd.read_excel(filepath, sheet_name='papers and inputs')
    bigrams = pd.DataFrame(columns=['bigrams', 'counts'])

    # Run through list of papers
    for i in df.index.values:

        # get authors of paper
        authors = list(df.columns.values[df.iloc[i, :] == 1])
        # get all possible combinations of 2 authors
        authors_bigrams = combinations(authors, 2)

        for big in authors_bigrams:
            # add to the count papers that the pair of authors worked together
            if big in list(bigrams.bigrams.values):
                bigrams.loc[bigrams['bigrams'] == big,
                            'counts'] = bigrams.loc[bigrams['bigrams'] == big, 'counts'] + 1
            else:
                # bigrams = bigrams.concat(pd.DataFrame([[big, 1]], columns=[
                #                          'bigrams', 'counts']), ignore_index=True)
                bigrams.loc[len(bigrams)] = [big, 1]

        print(f'    {i+1} out of {len(df.index.values)} papers')

    bigrams.to_csv('aux_files/bigrams.csv')
    return bigrams


def get_node_size_by_papers(G, filepath):

    # return dict with authors as keys and respective number of papers as values
    papers = pd.read_excel(filepath, sheet_name='papers and inputs')
    # papers.columns = [papers.columns[0]] + \
    # [f'{k.split(",")[1][0]}. {k.split(",")[0]}' for k in papers.columns[1:]]

    return {author: papers[author].astype(bool).sum(axis=0) for author in list(G.nodes)}


def get_affiliations(G, filepath, use_affiliations, colormap):

    if not use_affiliations:
        return None, None

    else:
        affil = pd.read_excel(
            filepath, sheet_name='input categories', usecols=[0, 1])

        # Change authors' names from "surname,name" to "n. surname"
        # for i in range(affil.shape[0]):
        #     affil.iloc[i,
        #                0] = f'{affil.iloc[i,0].split(",")[1][0]}. {affil.iloc[i,0].split(",")[0]}'

        # Reindex the dataframe to align with graph's nodes
        affil = affil.set_index('Input data')
        affil = affil.reindex(G.nodes())
        affil['Category'] = pd.Categorical(affil['Category'])
        affil['Category'].cat.codes

        # Normalize colormap to fit range of code values
        cdict = affil['Category'].cat.codes.to_dict()
        norm = mpl.colors.Normalize(vmin=0, vmax=max(list(cdict.values())))
        m = cm.ScalarMappable(norm=norm, cmap=colormap)

        # Create legend with color patches and respective affiliations
        legend = []
        for i in range(max(list(cdict.values()))+1):
            a = affil.loc[list(cdict.keys())[list(
                cdict.values()).index(i)], 'Category']
            legend += [mpatches.Patch(color=m.to_rgba(i), label=a)]

        node_color = affil['Category'].cat.codes

        return legend, node_color
