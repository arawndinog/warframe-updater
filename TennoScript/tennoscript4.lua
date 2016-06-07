local p = {}
 
local CharData = mw.loadData( 'Module:FactionScript/data' )

function p._tenno (humanwords,size)
	local humanwords = string.lower(humanwords)
	if (size == nil or size == '') then size='16' end
	local tennobet_list = {}
	local phonetic_list = {}
	local stack_list = {}
	local output_list = {}
	local i=string.len(humanwords)
	while i>0 do
		local this_char = humanwords:sub(i,i)
		local prev_char = humanwords:sub(i-1,i-1)
		if this_char == "h" then
			if (prev_char == "t" or
				prev_char == "d" or
				prev_char == "s" or
				prev_char == "z" or
				prev_char == "c" or
				prev_char == "k" or
				prev_char == "i" or
				prev_char == "e" or
				prev_char == "u") then
				table.insert(tennobet_list,CharData["TennoChar"][prev_char.."h"][1])
				table.insert(phonetic_list,CharData["TennoChar"][prev_char.."h"][2])
				i=i-2
			else
				table.insert(tennobet_list,CharData["TennoChar"]["h"][1])
				table.insert(phonetic_list,"c")
				i=i-1
			end
		elseif this_char == "g" then
			if prev_char == "n" then
				table.insert(tennobet_list,CharData["TennoChar"]["ng"][1])
				table.insert(phonetic_list,"c")
				i=i-2
			else
				table.insert(tennobet_list,CharData["TennoChar"]["g"][1])
				table.insert(phonetic_list,"c")
				i=i-1
			end
		elseif  this_char == "e" then
			if humanwords:sub(i-2,i-2)..prev_char == "ay" then
				table.insert(tennobet_list,CharData["TennoChar"]["aye"][1])
				i=i-3
			elseif (prev_char == "e" or
					prev_char == "a") then
				table.insert(tennobet_list,CharData["TennoChar"][prev_char.."e"][1])
				i=i-2
			else 
				table.insert(tennobet_list,CharData["TennoChar"]["e"][1])
				i=i-1
			end
			table.insert(phonetic_list,"v")
		elseif this_char == ("w") then
			if (prev_char == "a" or
				prev_char == "o") then
				i=i-2
			else
				table.insert(tennobet_list,CharData["TennoChar"]["oo"][1])
				i=i-1
			end
				table.insert(phonetic_list,"v")
		elseif this_char == ("o") then
			if prev_char == "o" then
				table.insert(tennobet_list,CharData["TennoChar"]["oo"][1])
				i=i-2
			else 
				table.insert(tennobet_list,CharData["TennoChar"]["o"][1])
				i=i-1
			end
				table.insert(phonetic_list,"v")
		elseif CharData["TennoChar"][this_char] ~= nil then
				table.insert(tennobet_list,CharData["TennoChar"][this_char][1])
				table.insert(phonetic_list,CharData["TennoChar"][this_char][2])
			i=i-1
		else
				table.insert(tennobet_list,"&nbsp;")
				table.insert(phonetic_list,"sp")
			i=i-1
		end
    end

    local j=#phonetic_list
	while j>0 do
	    if phonetic_list[j] == "c" then
            local stack_consonant = mw.html.create('div')
            :css('display','inline-block')
            :css('background','green')
            :css('margin','1px')
            :css('transform','rotate(25deg)')
            :wikitext("[[File:"..tennobet_list[j].."|link=]]"):done()
	    	table.insert(output_list,tostring(stack_consonant))
		    j=j-1
		elseif phonetic_list[j] == "s" then
            local stack_symbol = mw.html.create('div')
            :css('display','inline-block')
            :css('background','red')
            :css('margin','1px')
            :wikitext("[[File:"..tennobet_list[j].."|link=]]"):done()
		    table.insert(output_list,tostring(stack_symbol))
		    j=j-1
		elseif phonetic_list[j] == "v" then
		    local stack_vowel = mw.html.create('div')
            :css('display','inline-block')
            :css('background','blue')
            :css('transform','rotate(25deg)')
            :css('margin','1px'):done()
            repeat
                stack_vowel:wikitext("[[File:"..tennobet_list[j].."|link=]]"):done()
                j=j-1
            until phonetic_list[j] ~= "v"
		    table.insert(output_list,tostring(stack_vowel))
        else 
            local stack_space = mw.html.create('div')
            :css('display','inline-block')
            :css('background','orange')
            :css('margin','1px')
            :wikitext("&nbsp;"):done()
		    table.insert(output_list,tostring(stack_space))
		    j=j-1
	    end
	end
	return table.concat(output_list)
end

function p.tenno ( frame )
    local string_input = frame.args[1]
    local num_input = frame.args[2]
    return p._tenno(string_input,num_input)
end

return p