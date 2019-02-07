class NeighboursVisualization
{
	constructor()
	{
		this.selected_user = 'barackobama';
		this.selected_tweet_index = 0;
		this.progress = 1;		
	}

	getWordsInSelectedTweet()
	{
		return example_tweets[this.selected_user][this.selected_tweet_index].split(' ');
	}

	getTweetSoFar()
	{
		return this.getWordsInSelectedTweet().slice(0,this.progress).join(' ');	
	}

	updateProgressSlider()
	{
		$('#neighbours_progress_slider').attr('max',this.getWordsInSelectedTweet().length-1);

		this.progress = 1;
		$('#neighbours_progress_slider').val(this.progress);
	};

	updateTweetProgress()
	{
		var tweet_so_far = this.getTweetSoFar();
		var words = tweet_so_far.split(' ');

		if (words.length == 1)
		{
			last_words = words[0];
		}
		else if (words.length == 2)
		{
			last_words = words[0] + ' ' + words[1]; 
		}
		else
		{
			var last_words = words.slice(words.length-3,words.length)		
			last_words = last_words[0]+' '+last_words[1]+' '+last_words[2]			
		}

		tweet_so_far = tweet_so_far.replace(last_words,'<span class="lastwords">'+last_words+'</span>')

		$('#neighbours_vis .predicted_text').html(tweet_so_far+'|');
	}

	updateNeighbours()
	{
		var current_neighbours = nearest_neighbours[this.selected_user][this.selected_tweet_index][this.getTweetSoFar().length];

		var html = '<table>';

		for (var neighbour_index in current_neighbours)
		{
			var word1 = current_neighbours[neighbour_index][0][0];
			var word2 = current_neighbours[neighbour_index][0][1];
			var word3 = current_neighbours[neighbour_index][0][2];
			var prediction = current_neighbours[neighbour_index][1];

			var neighbour_index_plus_one = parseInt(neighbour_index)+1;

			html += '<tr><td class="number">'+neighbour_index_plus_one+'.</td><td><span class="lastwords">'+word1+' '+word2+' '+word3+'</span> &rarr; '+prediction+'</td></tr>';
		}

		html += '</table>';

		$('#neighbours_vis .neighbours_section').html(html);
	}

	updateEmbeddedTweet()
	{
		$('#neighbours_vis .embedded_tweet_area').html('<blockquote class="twitter-tweet" data-conversation="none" data-lang="en-gb"><p lang="en" dir="ltr"><a id="embedded_tweet" href="https://twitter.com/'+this.selected_user+'/status/'+scores_per_tweet[this.selected_user][this.selected_tweet_index]['id']+'"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><//script>')
	}
}

$(document).ready(function()
{
	console.log('neighbours ready');
	neighbours_vis = new NeighboursVisualization();

	$('#neighbours_vis .user_select').click(function()
	{
		$('#neighbours_vis .user_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		neighbours_vis.selected_user = $(this).attr('user');

		neighbours_vis.updateProgressSlider();
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updateNeighbours();
		neighbours_vis.updateEmbeddedTweet();		
	});

	$('#neighbours_vis .tweet_select').click(function()
	{
		$('#neighbours_vis .tweet_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		neighbours_vis.selected_tweet_index = $(this).attr('tweet_index')-1;

		neighbours_vis.updateProgressSlider();
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updateNeighbours();
		neighbours_vis.updateEmbeddedTweet();
	});

	$('#neighbours_vis #neighbours_progress_slider').on('input',function()
	{
		neighbours_vis.progress = parseInt($(this).val());
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updateNeighbours();
	});

	$('.arrow_left').click(function()
	{
		if (neighbours_vis.progress > 1)
		{
			neighbours_vis.progress -= 1;
		}
		
		$('#neighbours_progress_slider').val(neighbours_vis.progress);
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updateNeighbours();
	});

	$('.arrow_right').click(function()
	{
		if (neighbours_vis.progress < example_tweets[neighbours_vis.selected_user][neighbours_vis.selected_tweet_index].length)
		{
			neighbours_vis.progress += 1;
		}
		
		$('#neighbours_progress_slider').val(neighbours_vis.progress);
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updateNeighbours();
	});

	neighbours_vis.updateProgressSlider();
	neighbours_vis.updateTweetProgress();
	neighbours_vis.updateNeighbours();	
	neighbours_vis.updateEmbeddedTweet();		
});
