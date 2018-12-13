class EvalVisualization
{
	constructor()
	{
		this.selected_user = 'barackobama'
		this.selected_model = 'barackobama'
		this.selected_tweet_index = 0		
	}

	updateSelectedModel(model)
	{
		$('#eval_vis .model_select').each(function()
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

		$('#eval_vis #percentage_explanation').html('of the characters in this tweet were correctly predicted by the language model of @'+this.selected_model)
	}

	updateModelScores(user)
	{
		var bar_length_multiplier = 3;
		var score_per_language_model = eval_scores_per_language_model[user];
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

	updateExampleTweet(user,model,tweet_index)
	{
		var tweet_info = scores_per_tweet[user][tweet_index];

		$('#eval_vis .predicted_tweet_percentage').html(tweet_info['predicted_by'][model]['score']+'%')
		$('#eval_vis .predicted_tweet').html(tweet_info['predicted_by'][model]['text'])
		$('#eval_vis .embedded_tweet_area').html('<blockquote class="twitter-tweet" data-conversation="none" data-lang="en-gb"><p lang="en" dir="ltr"><a id="embedded_tweet" href="https://twitter.com/'+user+'/status/'+tweet_info['id']+'"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><//script>')
	}
}

$(document).ready(function()
{
	console.log('eval ready');

	eval_visualization = new EvalVisualization();

	$('#eval_vis .user_select').click(function()
	{
		$('#eval_vis .user_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		eval_visualization.selected_user = $(this).attr('user');

		eval_visualization.updateModelScores(eval_visualization.selected_user)	
		eval_visualization.updateSelectedModel(eval_visualization.selected_user)			
		eval_visualization.updateExampleTweet(eval_visualization.selected_user,eval_visualization.selected_model,eval_visualization.selected_tweet_index);
	});

	$('#eval_vis .model_select').click(function()
	{
		eval_visualization.updateSelectedModel($(this).attr('model'));
	});

	$('#eval_vis .tweet_select').click(function()
	{
		$('#eval_vis .tweet_select').each(function()
		{
			$(this).removeClass('selected');
		});

		$(this).addClass('selected');

		eval_visualization.selected_tweet_index = $(this).attr('tweet_index')-1;
		eval_visualization.updateExampleTweet(eval_visualization.selected_user,eval_visualization.selected_model,eval_visualization.selected_tweet_index);
	});

	eval_visualization.updateModelScores('barackobama');
	eval_visualization.updateExampleTweet('barackobama','barackobama',0);
});