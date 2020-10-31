Bracket builder
===========================

## How the app works

On the index page, there will be a `ul` of created brackets as `<a>` tags. Clicking on one of those will take you to the show page for that specific bracket. Follow the instructions below to craete a bracket.

### Creating Brackets

Beneath tthe list of brackets will be form to create a new bracket. Fill out the information with the following in mind:
1. The "Bracket theme" is essentially the name of the bracket. Example: the theme for our halloween bracket was "Scream and Stream"
2. "How big is the Bracket" means how many movies will be in this bracket. 
* this will always need to be an even number
* for example, our Scream and Stream bracket had 32 total movies in it.
3. "How many movies in the pool?" means, how many movies could potentially end up in the bracket.
* this number **must** be greater than, or equal to what you entered into the "How big is the Bracket" field.
* for example, the next contest we run will be our "Sequels watch party (theme tbd)" and we have a "pool" of 43 movies that will be randomly drawn into our bracket of 32 movies.

Once you navigate to a bracket show page, *if* there are movies in the pool there will be display of all the movies in the pool. If you have not entered an movies into the pool, there will be a bunch of inputs where you can enter the movies that will go into the pool. 

### How to enter movies into the pool

1. Enter each movie title into the feild labeled "Movie `foo` title" (obviously)
2. Enter the amount of votes each movie got. The deafault amount of votes is 1
* The number of votes is essentially a multiplier making that specific movie more likely to end up in the bracket. This will make more sense when we talk about how the bracket gets filled out.
3. Once all the info is entered, hit submit to enter the movies into the pool and launch the script.
* At some point, I'm gonna refactor this so it only enters the movies into the pool and there will be a seperate button to run the bracket builder script.

### How the script works

and *if* the bracket has been created, there will be a display of the bracket and all the matchups. If the bracket *is not* filled out, 


