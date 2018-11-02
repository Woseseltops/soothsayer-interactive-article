var selected_user = 'barackobama'
var selected_model = 'barackobama'
var selected_tweet_index = 0

function updateModelScores(user)
{
	var bar_length_multiplier = 3;
	var score_per_language_model = scores_per_language_model[user];
	var c = 0;

	//Change the names for each of the predictors, and hide otherwise
	$('#eval_vis .predictor_name').each(function()
	{
		if (score_per_language_model.length > c)
		{
			$(this).html('@'+score_per_language_model[c][0]);
			$(this).parent().parent().show();
		}
		else
		{
			$(this).parent().parent().hide();
		}
		c++;
	});

	//Changes the scores
	c = 0
	$('#eval_vis .predictor_score').each(function()
	{
		if (score_per_language_model.length > c)
		{
			$(this).html(score_per_language_model[c][1]+'%');
			c++;
		}
	});

	//Change the photos
	c = 0
	$('#eval_vis .predictor_picture').each(function()
	{
		if (score_per_language_model.length > c)
		{
			$(this).attr('src','img/'+score_per_language_model[c][0]+'.jpg');
			$(this).attr('model',''+score_per_language_model[c][0]);
			c++;
		}
	});

	//Change the bar
	c = 0
	$('#eval_vis .bar').each(function()
	{
		if (score_per_language_model.length > c)
		{
			$(this).css('width',bar_length_multiplier*score_per_language_model[c][1]+'px');
			c++;
		}
	});			
}

function updateExampleTweet(user,model,tweet_index)
{
	var tweet_info = scores_per_tweet[user][tweet_index];

	$('#eval_vis .predicted_tweet_percentage').html(tweet_info['predicted_by'][model]['score']+'%')
	$('#eval_vis .predicted_tweet').html(tweet_info['predicted_by'][model]['text'])
	$('#eval_vis .embedded_tweet_area').html('<blockquote class="twitter-tweet" data-conversation="none" data-lang="en-gb"><p lang="en" dir="ltr"><a id="embedded_tweet" href="https://twitter.com/'+user+'/status/'+tweet_info['id']+'"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><//script>')
}

$(document).ready(function()
{
	$('#eval_vis .user_select').click(function()
	{
		$('#eval_vis .user_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		selected_user = $(this).attr('user');

		//It can happen that you're switching to a user for which the current model doesn't have predictions
		if (!(selected_model in scores_per_tweet[selected_user][0]['predicted_by']))
		{
			selected_model = selected_user;	
		}

		updateExampleTweet(selected_user,selected_model,selected_tweet_index);
		updateModelScores(selected_user)				
	});

	$('#eval_vis .model_select').click(function()
	{
		$('#eval_vis .model_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		selected_model = $(this).attr('model');
		updateExampleTweet(selected_user,selected_model,selected_tweet_index);

		$('#percentage_explanation').html('of the characters in this tweet were correctly predicted by the language model of @'+selected_model)
	});

	$('#eval_vis .tweet_select').click(function()
	{
		$('#eval_vis .tweet_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		selected_tweet_index = $(this).attr('tweet_index')-1;
		updateExampleTweet(selected_user,selected_model,selected_tweet_index);
	});

	updateModelScores('barackobama');
	updateExampleTweet('barackobama','barackobama',0);
});