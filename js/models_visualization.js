class ModelsVisualization
{
	constructor()
	{
		this.selected_user = 'barackobama';
		this.selected_tweet_index = 0;
		this.progress = 1;		
	}

	updateProgressSlider()
	{
		$('#models_progress_slider').attr('max',example_tweets[this.selected_user][this.selected_tweet_index].length);

		this.progress = 1;
		$('#models_progress_slider').val(this.progress);
	};

	updateTweetProgress()
	{
		var progress_text = example_tweets[this.selected_user][this.selected_tweet_index].substring(0,this.progress);
		$('#models_vis .predicted_text').html(progress_text+'|');
	}

	updatePredictions()
	{
		var predictions_for_this_user = predictions_per_language_model[this.selected_user]
		var models = ['barackobama','jtimberlake','kimkardashian','ladygaga'];

		for (var model_index in models)
		{
			var model = models[model_index]
			var predictions = predictions_for_this_user[model][this.selected_tweet_index][this.progress-1];

			var maximum_prediction_length = 9;

			if (predictions[0] != null)
			{
				predictions[0] = predictions[0].substring(0,maximum_prediction_length)				
			}

			if (predictions[1] != null)
			{
				predictions[1] = predictions[1].substring(0,maximum_prediction_length)				
			}

			if (predictions[2] != null)
			{
				predictions[2] = predictions[2].substring(0,maximum_prediction_length)				
			}

			$('#prediction_'+model+'_1').html(predictions[0]);
			$('#prediction_'+model+'_2').html(predictions[1]);
			$('#prediction_'+model+'_3').html(predictions[2]);

		}
	}

	updateEmbeddedTweet()
	{
		$('#models_vis .embedded_tweet_area').html('<blockquote class="twitter-tweet" data-conversation="none" data-lang="en-gb"><p lang="en" dir="ltr"><a id="embedded_tweet" href="https://twitter.com/'+this.selected_user+'/status/'+scores_per_tweet[this.selected_user][this.selected_tweet_index]['id']+'"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><//script>')
	}
}

$(document).ready(function()
{
	console.log('models ready');
	models_vis = new ModelsVisualization();

	$('#models_vis .user_select').click(function()
	{
		$('#models_vis .user_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		models_vis.selected_user = $(this).attr('user');

		models_vis.updateProgressSlider();
		models_vis.updateTweetProgress();
		models_vis.updatePredictions();
		models_vis.updateEmbeddedTweet();
	});

	$('#models_vis .tweet_select').click(function()
	{
		$('#models_vis .tweet_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		models_vis.selected_tweet_index = $(this).attr('tweet_index')-1;

		models_vis.updateProgressSlider();
		models_vis.updateTweetProgress();
		models_vis.updatePredictions();
		models_vis.updateEmbeddedTweet();
	});

	$('#models_vis #models_progress_slider').on('input',function()
	{
		models_vis.progress = parseInt($(this).val());
		models_vis.updateTweetProgress();
		models_vis.updatePredictions();
	});

	$('.arrow_left').click(function()
	{
		if (models_vis.progress > 1)
		{
			models_vis.progress -= 1;
		}
		
		$('#models_progress_slider').val(models_vis.progress);
		models_vis.updateTweetProgress();
		models_vis.updatePredictions();
	});

	$('.arrow_right').click(function()
	{
		if (models_vis.progress < example_tweets[models_vis.selected_user][models_vis.selected_tweet_index].length)
		{
			models_vis.progress += 1;
		}
		
		$('#models_progress_slider').val(models_vis.progress);
		models_vis.updateTweetProgress();
		models_vis.updatePredictions();
	});

	models_vis.updateProgressSlider();
	models_vis.updateTweetProgress();
	models_vis.updatePredictions();	
	models_vis.updateEmbeddedTweet();		
});
