import autocomplete

# load pickled python Counter objects representing our predictive models
# I use Peter Norvigs big.txt (http://norvig.com/big.txt) to create the predictive models
autocomplete.load()
autocomplete.run_server()
# imagine writing "the b"
autocomplete.predict('the','b')

arr = [('blood', 204),
 ('battle', 185),
 ('bone', 175),
 ('best', 149),
 ('body', 149)]

# now you type an "o"

autocomplete.predict('the','bo')

[('bone', 175),
 ('body', 149),
 ('bones', 122),
 ('boy', 46),
 ('bottom', 32),
 ('box', 24),
 ...]