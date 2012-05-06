%rebase tpl/base title='party'
<p class="summary"><a href="/help/{{network}}/">help</a> | <a href="..">additional parties</a></p>

<div class="section party">
    <div class="heading">
        <h3>party</h3>
    </div>
    <div class="key">
        <p>{{party['nick']}}</p>
        <p>via {{len(party['lines'])-2}}</p>
    </div>
    <div class="item phrases">
    %for line in party['lines']:
        <p>{{line}}</p>
    %end
    </div>
</div>