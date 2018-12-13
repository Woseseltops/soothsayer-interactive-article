class SociolectVisualization
{
	constructor()
	{
		this.selected_user = 'barackobama'
		this.selected_model = 'barackobama'
		this.selected_tweet_index = 0		
	}	

	updateSelectedModel(model)
	{
		$('#sociolect_vis .model_select').each(function()
		{
			if ($(this).attr('model') == model)
			{
				$(this).addClass('selected');
			} 
			else
			{
				$(this).removeClass('selected');
			}
		});

		this.selected_model = model
		this.updateExampleTweet(this.selected_user,this.selected_model,this.selected_tweet_index);

		console.log(this.selected_model)

		$('#sociolect_vis #percentage_explanation').html('of the characters in this tweet were correctly predicted by the language model of @'+this.selected_model)
	}

	updateModelScores(user)
	{
		var bar_length_multiplier = 3;
		var score_per_language_model = sociolect_scores_per_language_model[user];
		var c = 0;

		//Change the names for each of the predictors, and hide otherwise
		$('#sociolect_vis .predictor_name').each(function()
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
		$('#sociolect_vis .predictor_score').each(function()
		{
			if (score_per_language_model.length > c)
			{
				$(this).html(score_per_language_model[c][1]+'%');
				c++;
			}
		});

		//Change the photos
		c = 0
		$('#sociolect_vis .predictor_picture').each(function()
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
		$('#sociolect_vis .bar').each(function()
		{
			if (score_per_language_model.length > c)
			{
				$(this).css('width',bar_length_multiplier*score_per_language_model[c][1]+'px');
				c++;
			}
		});			
	}

	updateExampleTweet(user,model,tweet_index)
	{
		var tweet_info = scores_per_tweet[user][tweet_index];

		$('#sociolect_vis .predicted_tweet_percentage').html(tweet_info['predicted_by'][model]['score']+'%')
		$('#sociolect_vis .predicted_tweet').html(tweet_info['predicted_by'][model]['text'])
		$('#sociolect_vis .embedded_tweet_area').html('<blockquote class="twitter-tweet" data-conversation="none" data-lang="en-gb"><p lang="en" dir="ltr"><a id="embedded_tweet" href="https://twitter.com/'+user+'/status/'+tweet_info['id']+'"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><//script>')
	}
}

$(document).ready(function()
{
	console.log('socio ready');

	sociolect_vis = new SociolectVisualization();

	$('#sociolect_vis .user_select').click(function()
	{
		$('#sociolect_vis .user_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		sociolect_vis.selected_user = $(this).attr('user');

		sociolect_vis.updateModelScores(sociolect_vis.selected_user)	
		sociolect_vis.updateSelectedModel(sociolect_vis.selected_user)			
		sociolect_vis.updateExampleTweet(sociolect_vis.selected_user,sociolect_vis.selected_model,sociolect_vis.selected_tweet_index);
	});

	$('#sociolect_vis .model_select').click(function()
	{
		sociolect_vis.updateSelectedModel($(this).attr('model'));
	});

	$('#sociolect_vis .tweet_select').click(function()
	{
		$('#sociolect_vis .tweet_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		sociolect_vis.selected_tweet_index = $(this).attr('tweet_index')-1;
		sociolect_vis.updateExampleTweet(sociolect_vis.selected_user,sociolect_vis.selected_model,sociolect_vis.selected_tweet_index);
	});

	sociolect_vis.updateModelScores('barackobama');
	sociolect_vis.updateExampleTweet('barackobama','barackobama',0);
});