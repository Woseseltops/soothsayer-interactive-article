class NeighboursVisualization
{
	constructor()
	{
		this.selected_user = 'barackobama';
		this.selected_tweet_index = 0;
		this.progress = 1;		
	}

	updateProgressSlider()
	{
		console.log('update progress')

		$('#neighbours_progress_slider').attr('max',example_tweets[this.selected_user][this.selected_tweet_index].length);

		this.progress = 1;
		$('#neighbours_progress_slider').val(this.progress);
	};

	updateTweetProgress()
	{
		var progress_text = example_tweets[this.selected_user][this.selected_tweet_index].substring(0,this.progress);
		$('#neighbours_vis .predicted_text').html(progress_text+'|');
	}

	updatePredictions()
	{
		var predictions_for_this_user = predictions_per_language_model[this.selected_user]
		var models = ['barackobama','jtimberlake','kimkardashian','ladygaga'];

		for (var model_index in models)
		{
			var model = models[model_index]
			var predictions = predictions_for_this_user[model][this.selected_tweet_index][this.progress-1];
			$('#'+model+'_predictions').html(predictions.join(', '))
		}
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
		neighbours_vis.updatePredictions();
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
		neighbours_vis.updatePredictions();
		neighbours_vis.updateEmbeddedTweet();
	});

	$('#neighbours_vis #neighbours_progress_slider').on('input',function()
	{
		neighbours_vis.progress = parseInt($(this).val());
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updatePredictions();
	});

	$('.arrow_left').click(function()
	{
		if (neighbours_vis.progress > 1)
		{
			neighbours_vis.progress -= 1;
		}
		
		$('#neighbours_progress_slider').val(neighbours_vis.progress);
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updatePredictions();
	});

	$('.arrow_right').click(function()
	{
		if (neighbours_vis.progress < example_tweets[neighbours_vis.selected_user][neighbours_vis.selected_tweet_index].length)
		{
			neighbours_vis.progress += 1;
		}
		
		$('#neighbours_progress_slider').val(neighbours_vis.progress);
		neighbours_vis.updateTweetProgress();
		neighbours_vis.updatePredictions();
	});

	neighbours_vis.updateProgressSlider();
	neighbours_vis.updateTweetProgress();
	neighbours_vis.updatePredictions();	
	neighbours_vis.updateEmbeddedTweet();		
});
