var selected_user = 'barackobama';
var selected_tweet_index = 0;
var progress = 1;

function updateProgressSlider()
{
	$('#progress_slider').attr('max',example_tweets[selected_user][selected_tweet_index].length);

	progress = 1;
	$('#progress_slider').val(progress);
};

function updateTweetProgress()
{
	var progress_text = example_tweets[selected_user][selected_tweet_index].substring(0,progress);
	$('#models_vis .predicted_text').html(progress_text+'|');
}

function updatePredictions()
{
	predictions_for_this_user = predictions_per_language_model[selected_user]
	var models = ['barackobama','jtimberlake','kimkardashian','ladygaga'];

	for (model_index in models)
	{
		var model = models[model_index]
		var predictions = predictions_for_this_user[model][selected_tweet_index][progress-1];
		$('#'+model+'_predictions').html(predictions.join(', '))
	}
}

function updateEmbeddedTweet()
{
	$('#models_vis .embedded_tweet_area').html('<blockquote class="twitter-tweet" data-conversation="none" data-lang="en-gb"><p lang="en" dir="ltr"><a id="embedded_tweet" href="https://twitter.com/'+selected_user+'/status/'+scores_per_tweet[selected_user][selected_tweet_index]['id']+'"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><//script>')
}

$(document).ready(function()
{
	$('#models_vis .user_select').click(function()
	{
		$('#models_vis .user_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		selected_user = $(this).attr('user');

		updateProgressSlider();
		updateTweetProgress();
		updatePredictions();
		updateEmbeddedTweet();
	});

	$('#models_vis .tweet_select').click(function()
	{
		$('#models_vis .tweet_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		selected_tweet_index = $(this).attr('tweet_index')-1;

		updateProgressSlider();
		updateTweetProgress();
		updatePredictions();
		updateEmbeddedTweet();
	});

	$('#models_vis #progress_slider').on('input',function()
	{
		progress = parseInt($(this).val());
		updateTweetProgress();
		updatePredictions();
	});

	$('.arrow_left').click(function()
	{
		if (progress > 1)
		{
			progress -= 1;
		}
		
		$('#progress_slider').val(progress);
		updateTweetProgress();
		updatePredictions();
	});

	$('.arrow_right').click(function()
	{
		if (progress < example_tweets[selected_user][selected_tweet_index].length)
		{
			progress += 1;
		}
		
		$('#progress_slider').val(progress);
		updateTweetProgress();
		updatePredictions();
	});

	updateProgressSlider();
	updateTweetProgress();
	updatePredictions();	
	updateEmbeddedTweet();		
});
